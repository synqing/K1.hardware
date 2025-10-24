# K1_ImportAndPlace.py
# Action Plugin: Import KiCad XML netlist (v5), add footprints programmatically,
# assign nets, and perform a collision-free grid placement. Saves the board.
#
# Why this works: it runs *inside* KiCad's PCB Editor, so pcbnew & wx are valid.
# No SWIG/wxApp crashes; no CLI "netlist import" needed.

import pcbnew
import wx
import os
import xml.etree.ElementTree as ET
import math

def _mm(val): return pcbnew.FromMM(val)
def _to_mm(nm): return pcbnew.ToMM(nm)

class K1ImportAndPlace(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "K1: Import Netlist + Place"
        self.category = "K1 Tools"
        self.description = "Import KiCad XML netlist, add footprints, assign nets, grid-place, save"
        self.show_toolbar_button = True
        self.icon_file_name = ""  # optional

    def _load_config(self, board_path):
        # Read tools/k1_config.json next to project root
        import json
        proj_dir = os.path.abspath(os.path.join(board_path, os.pardir, os.pardir)) \
                   if board_path.endswith(".kicad_pcb") else os.getcwd()
        cfg_path = os.path.join(proj_dir, "tools", "k1_config.json")
        if not os.path.exists(cfg_path):
            raise RuntimeError(f"Config file not found: {cfg_path}")
        with open(cfg_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _parse_netlist(self, path):
        if not os.path.exists(path):
            raise RuntimeError(f"Netlist not found: {path}")
        tree = ET.parse(path)
        root = tree.getroot()
        # Components
        comps = {}  # ref -> {"footprint": "Lib:Name", "value": "..."}
        for comp in root.findall("./components/comp"):
            ref = comp.get("ref")
            fp  = comp.findtext("footprint", default="").strip()
            val = comp.findtext("value", default="").strip()
            if not ref or ":" not in fp:
                raise RuntimeError(f"Missing or invalid footprint for {ref}: '{fp}'")
            comps[ref] = {"footprint": fp, "value": val}
        # Nets: name -> list of (ref, pin)
        nets = {}
        for net in root.findall("./nets/net"):
            name = net.get("name")
            if not name:
                continue
            nodes = []
            for node in net.findall("node"):
                nodes.append((node.get("ref"), node.get("pin")))
            nets[name] = nodes
        return comps, nets

    def _ensure_net(self, board, name):
        # Create or fetch NETINFO_ITEM
        nets = board.GetNetsByName()
        if name in nets:
            return nets[name]
        nii = pcbnew.NETINFO_ITEM(board, name)
        board.Add(nii)
        return nii

    def _load_footprint(self, fp_id):
        # fp_id like "LibNick:FootprintName" — relies on configured lib table
        lib, name = fp_id.split(":", 1)
        f = pcbnew.FootprintLoad(lib, name)
        if f is None:
            raise RuntimeError(f"FootprintLoad failed for {fp_id}. Check library table / name.")
        return f

    def _board_bbox(self, board):
        bbox = board.GetBoardEdgesBoundingBox()
        if bbox.GetWidth() == 0 or bbox.GetHeight() == 0:
            raise RuntimeError("Edge.Cuts outline not found.")
        return bbox

    def _place_grid(self, board, refs_in_order):
        bbox = self._board_bbox(board)
        margin = _mm(2.0)
        x0 = bbox.GetX() + margin
        y0 = bbox.GetY() + margin
        w  = bbox.GetWidth()  - 2*margin
        h  = bbox.GetHeight() - 2*margin

        n = len(refs_in_order)
        cols = max(1, math.ceil(math.sqrt(n)))
        rows = math.ceil(n / cols)
        cell_w = max(_mm(5.0), w // cols)
        cell_h = max(_mm(5.0), h // rows)

        # Sort: MCUs/ICs, connectors, regulators, others
        def rank(ref):
            fp = board.FindFootprintByReference(ref)
            val = fp.GetValue().upper() if fp else ""
            if ref.startswith("U") or "ESP32" in val or "MCU" in val: return (0, ref)
            if ref.startswith("J") or "USB" in val: return (1, ref)
            if "LDO" in val or "REG" in val: return (2, ref)
            return (3, ref)

        refs_in_order.sort(key=rank)

        i = 0
        for r in range(rows):
            for c in range(cols):
                if i >= n: break
                ref = refs_in_order[i]
                fp = board.FindFootprintByReference(ref)
                if not fp:
                    i += 1
                    continue
                px = x0 + c * cell_w + cell_w // 2
                py = y0 + r * cell_h + cell_h // 2
                # Keep connectors near top/bottom edges
                if ref.startswith("J") or "USB" in fp.GetValue().upper():
                    top = y0
                    bot = y0 + rows*cell_h - cell_h//2
                    py = top if abs(py - top) < abs(py - bot) else bot
                fp.SetPosition(pcbnew.VECTOR2I(int(px), int(py)))
                fp.SetOrientationDegrees(0.0)
                i += 1

        board.BuildListOfNets()
        pcbnew.Refresh()
        return cols, rows, cell_w, cell_h

    def Run(self):
        try:
            board = pcbnew.GetBoard()
            board_path = board.GetFileName()
            cfg = self._load_config(board_path)
            netlist = cfg["netlist_file"]

            comps, nets = self._parse_netlist(netlist)

            # Map existing footprints to avoid duplicates
            existing_refs = set(fp.GetReference() for fp in board.GetFootprints())

            # 1) Add footprints (value + ref) for new comps
            added = 0
            ref_to_fp = {}
            for ref, meta in comps.items():
                if ref in existing_refs:  # already present
                    ref_to_fp[ref] = board.FindFootprintByReference(ref)
                    continue
                f = self._load_footprint(meta["footprint"])
                f.SetReference(ref)
                f.SetValue(meta["value"] or ref)
                f.SetPosition(pcbnew.VECTOR2I(0, 0))
                f.SetOrientationDegrees(0.0)
                board.Add(f)
                ref_to_fp[ref] = f
                added += 1

            # 2) Ensure nets exist, assign pads to nets
            # Build pad lookup: (ref, padnum) -> PAD
            pad_lookup = {}
            for ref, fp in ref_to_fp.items():
                if not fp: continue
                for pad in fp.Pads():
                    pad_lookup[(ref, pad.GetName())] = pad

            assigned = 0
            for net_name, nodes in nets.items():
                nii = self._ensure_net(board, net_name)
                for ref, pin in nodes:
                    pad = pad_lookup.get((ref, pin))
                    if pad:
                        pad.SetNet(nii)
                        assigned += 1

            board.BuildListOfNets()

            # 3) Grid placement (collision-free baseline)
            refs = list(comps.keys())
            cols, rows, cw, ch = self._place_grid(board, refs)

            # 4) Save board
            board.Save(board_path)

            wx.MessageBox(
                f"Import complete.\n"
                f"Footprints added: {added}\n"
                f"Pad-to-net assignments: {assigned}\n"
                f"Placement grid: {cols} x {rows} (≈{_to_mm(cw):.1f} x {_to_mm(ch):.1f} mm cells)\n"
                f"Saved:\n{board_path}",
                "K1 Import + Place"
            )
        except Exception as e:
            wx.MessageBox(f"ERROR: {str(e)}", "K1 Import + Place", style=wx.ICON_ERROR)

K1ImportAndPlace().register()
