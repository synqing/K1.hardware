
# K1_ContractedPlace.py
# Contract-driven placement plugin:
# - Reads tools/k1_project.json (Design Contract)
# - Ensures board outline exists (draws rectangle if missing)
# - Places mounting holes (uses standard MountingHole footprints)
# - Places edge connectors along specified edges (even spacing)
# - Places main components into their zones
# - Applies copper/mask keepouts for antenna, etc.
#
# Run inside KiCad PCB Editor: Tools -> External Plugins -> K1: Contracted Place

import pcbnew
import wx
import os, json, math

MM = pcbnew.FromMM
def toMM(nm): return pcbnew.ToMM(nm)

EDGE = pcbnew.Edge_Cuts

def _repo_root(board_path):
    cur = os.path.dirname(os.path.abspath(board_path))
    for _ in range(5):
        cand = os.path.join(cur, "tools", "k1_project.json")
        if os.path.exists(cand):
            return cur
        cur = os.path.dirname(cur)
    raise RuntimeError("Could not locate tools/k1_project.json near the board.")

def _contract(board_path):
    root = _repo_root(board_path)
    p = os.path.join(root, "tools", "k1_project.json")
    with open(p,"r",encoding="utf-8") as f:
        return json.load(f), p

def _ensure_outline(board, w_mm, h_mm, cr_mm=0.0):
    bbox = board.GetBoardEdgesBoundingBox()
    if bbox.GetWidth() > 0 and bbox.GetHeight() > 0:
        return False  # already present
    # Draw rectangle from (0,0)
    def seg(x1,y1,x2,y2):
        ds = pcbnew.PCB_SHAPE(board)
        ds.SetShape(pcbnew.SHAPE_T_SEGMENT)
        ds.SetLayer(EDGE)
        ds.SetStart(pcbnew.VECTOR2I(MM(x1), MM(y1)))
        ds.SetEnd(  pcbnew.VECTOR2I(MM(x2), MM(y2)))
        board.Add(ds)
    seg(0,0, w_mm,0)
    seg(w_mm,0, w_mm,h_mm)
    seg(w_mm,h_mm, 0,h_mm)
    seg(0,h_mm, 0,0)
    return True

def _load_mounting_footprint(dia):
    # Use KiCad std library name; user must have "MountingHole" lib
    size = f"MountingHole_{dia:.1f}mm_M3" if abs(dia-3.2)<0.31 else f"MountingHole_{dia:.1f}mm"
    lib = "MountingHole"
    return lib, size

def _place_mounting_holes(board, holes):
    added = 0
    for h in holes:
        lib, mod = _load_mounting_footprint(h["diameter"])
        fp = pcbnew.FootprintLoad(lib, mod)
        if not fp:
            raise RuntimeError(f"Missing footprint {lib}:{mod} for mounting hole.")
        fp.SetReference(f"H{added+1}")
        fp.SetPosition(pcbnew.VECTOR2I(MM(h["x"]), MM(h["y"])))
        fp.SetOrientationDegrees(0.0)
        board.Add(fp)
        added += 1
    return added

def _edge_vec(board, edge, margin_mm=1.0):
    bbox = board.GetBoardEdgesBoundingBox()
    if edge == "north":
        y = bbox.GetY() + MM(margin_mm)
        return ("h", y, bbox.GetX() + MM(margin_mm), bbox.GetX()+bbox.GetWidth()-MM(margin_mm))
    if edge == "south":
        y = bbox.GetY() + bbox.GetHeight() - MM(margin_mm)
        return ("h", y, bbox.GetX() + MM(margin_mm), bbox.GetX()+bbox.GetWidth()-MM(margin_mm))
    if edge == "west":
        x = bbox.GetX() + MM(margin_mm)
        return ("v", x, bbox.GetY() + MM(margin_mm), bbox.GetY()+bbox.GetHeight()-MM(margin_mm))
    if edge == "east":
        x = bbox.GetX() + bbox.GetWidth() - MM(margin_mm)
        return ("v", x, bbox.GetY() + MM(margin_mm), bbox.GetY()+bbox.GetHeight()-MM(margin_mm))
    raise RuntimeError(f"Unknown edge: {edge}")

def _place_on_edge(board, ref, edge, offset_mm=0.0):
    fp = board.FindFootprintByReference(ref)
    if not fp:
        return False
    orient, f, a, b = _edge_vec(board, edge, margin_mm=1.0)
    if orient == "h":
        cx = int((a+b)//2 + MM(offset_mm))
        cy = int(f)
        fp.SetPosition(pcbnew.VECTOR2I(cx, cy))
        fp.SetOrientationDegrees(180.0 if edge=="north" else 0.0)
    else:
        cy = int((a+b)//2 + MM(offset_mm))
        cx = int(f)
        fp.SetPosition(pcbnew.VECTOR2I(cx, cy))
        fp.SetOrientationDegrees(90.0 if edge=="west" else -90.0)
    return True

def _spread_along_edge(board, refs, edge, margin_mm=6.0):
    placed = 0
    orient, f, a, b = _edge_vec(board, edge, margin_mm=margin_mm)
    n = len(refs)
    for i, ref in enumerate(refs):
        fp = board.FindFootprintByReference(ref)
        if not fp:
            continue
        t = (i+1)/(n+1)
        if orient == "h":
            x = int(a + t*(b-a))
            y = int(f)
            fp.SetPosition(pcbnew.VECTOR2I(x, y))
            fp.SetOrientationDegrees(180.0 if edge=="north" else 0.0)
        else:
            y = int(a + t*(b-a))
            x = int(f)
            fp.SetPosition(pcbnew.VECTOR2I(x, y))
            fp.SetOrientationDegrees(90.0 if edge=="west" else -90.0)
        placed += 1
    return placed

def _place_zone_center(board, refs, x_mm, y_mm, w_mm, h_mm, rot=0.0):
    cx = MM(x_mm + w_mm/2.0); cy = MM(y_mm + h_mm/2.0)
    count = 0
    for ref in refs:
        fp = board.FindFootprintByReference(ref)
        if not fp: 
            continue
        fp.SetPosition(pcbnew.VECTOR2I(int(cx), int(cy)))
        fp.SetOrientationDegrees(rot)
        count += 1
    return count

def _add_keepout_rect(board, x, y, w, h, layers_names):
    # create a rectangular keepout for copper/mask/paste
    rect = pcbnew.PCB_SHAPE(board)
    rect.SetShape(pcbnew.SHAPE_T_RECT)
    rect.SetLayer(pcbnew.F_Cu)  # layer is symbolic for container; we set layerset on keepout settings
    rect.SetRect(pcbnew.EDA_RECT(
        pcbnew.VECTOR2I(MM(x), MM(y)),
        pcbnew.VECTOR2I(MM(x+w), MM(y+h))
    ))
    ko = pcbnew.KEEPOUT_AREA(board)
    ko.SetBoundingBox(rect.GetRect())
    # Apply to specified layers
    lset = pcbnew.LSET()
    for nm in layers_names:
        lid = board.GetLayerID(nm)
        if lid != pcbnew.UNDEFINED_LAYER:
            lset.AddLayer(lid)
    ko.SetLayerSet(lset)
    ko.SetDoNotAllowTracks(True)
    ko.SetDoNotAllowVias(True)
    ko.SetDoNotAllowCopperPour(True)
    board.Add(ko)

class K1ContractedPlace(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "K1: Contracted Place (Design Contract)"
        self.category = "K1 Tools"
        self.description = "Apply k1_project.json: outline, holes, edge connectors, zones, keepouts; then save"
        self.show_toolbar_button = True
        self.icon_file_name = ""

    def Run(self):
        try:
            board = pcbnew.GetBoard()
            bp = board.GetFileName()
            cfg, cfg_path = _contract(bp)

            mech = cfg["mechanical"]
            w = float(mech["outline"]["width"]); h = float(mech["outline"]["height"])
            cr = float(mech["outline"].get("corner_radius", 0.0))
            created = _ensure_outline(board, w, h, cr)

            holes = mech.get("mounting_holes", [])
            added_holes = _place_mounting_holes(board, holes) if holes else 0

            io = cfg.get("io", {})
            # USB
            usb = io.get("usb")
            if usb and usb.get("ref"):
                _place_on_edge(board, usb["ref"], usb.get("edge","south"), usb.get("offset_mm",0.0))
            # LED ports
            leds = io.get("led_ports")
            led_count = 0
            if leds and leds.get("refs"):
                led_count = _spread_along_edge(board, leds["refs"], leds.get("edge","north"), leds.get("margin_mm",6.0))

            # Zones for key modules
            zones = cfg.get("placement_zones", [])
            zoned = 0
            for z in zones:
                zoned += _place_zone_center(board, z.get("refs",[]), z["x"], z["y"], z["w"], z["h"], z.get("rotation",0.0))

            # Keepouts
            for ko in mech.get("keepouts", []):
                _add_keepout_rect(board, ko["x"], ko["y"], ko["w"], ko["h"], ko.get("layers",["F.Cu","B.Cu"]))

            board.BuildListOfNets()
            board.Save(bp)

            wx.MessageBox(
                "Contract applied.\n"
                f"Outline created: {created}\n"
                f"Mounting holes added: {added_holes}\n"
                f"LED ports placed: {led_count}\n"
                f"Zoned refs placed: {zoned}\n"
                f"Config: {cfg_path}",
                "K1: Contracted Place"
            )
        except Exception as e:
            wx.MessageBox(f"ERROR: {e}", "K1: Contracted Place", style=wx.ICON_ERROR)

K1ContractedPlace().register()
