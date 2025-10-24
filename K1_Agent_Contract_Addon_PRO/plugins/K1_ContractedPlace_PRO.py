
# K1_ContractedPlace_PRO.py
# Contract-driven, advanced placement & prep:
# - Reads tools/k1_project_v2.json
# - Outline + holes + keepouts + edge placements + zone placements
# - Auto-decoupler placement near IC power pads
# - Edge GND via ring
# - SPI guard corridor (GND stitching via lines from COM_A to COM_B)
# - Netclasses for SPI/USB (width/clearance/diff)
# - Optional power planes (basic rectangular zones)
# - Optional thermal via grids under hot parts
# - Optional testpoints on named nets
#
# Run inside KiCad PCB Editor (Tools -> External Plugins -> K1: Contracted Place PRO)

import pcbnew
import wx
import os, json, math

MM = pcbnew.FromMM
def toMM(nm): return pcbnew.ToMM(nm)
EDGE = pcbnew.Edge_Cuts

# ---------- utilities ----------
def repo_root_from(board_path, rel="tools/k1_project_v2.json"):
    cur = os.path.dirname(os.path.abspath(board_path))
    for _ in range(6):
        cand = os.path.join(cur, rel)
        if os.path.exists(cand): return cur
        cur = os.path.dirname(cur)
    raise RuntimeError(f"Could not find {rel} relative to {board_path}")

def read_json(path):
    with open(path,"r",encoding="utf-8") as f: return json.load(f)

def ensure_net(board, name):
    by = board.GetNetsByName()
    if name in by: return by[name]
    nii = pcbnew.NETINFO_ITEM(board, name)
    board.Add(nii); return nii

def board_bbox(board): 
    bb = board.GetBoardEdgesBoundingBox()
    if bb.GetWidth() == 0 or bb.GetHeight() == 0:
        raise RuntimeError("Edge.Cuts outline missing.")
    return bb

def add_edge_rect(board, w_mm, h_mm):
    bb = board.GetBoardEdgesBoundingBox()
    if bb.GetWidth() and bb.GetHeight(): return False
    def seg(x1,y1,x2,y2):
        s = pcbnew.PCB_SHAPE(board); s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetLayer(EDGE)
        s.SetStart(pcbnew.VECTOR2I(MM(x1),MM(y1)))
        s.SetEnd(  pcbnew.VECTOR2I(MM(x2),MM(y2)))
        board.Add(s)
    seg(0,0,w_mm,0); seg(w_mm,0,w_mm,h_mm); seg(w_mm,h_mm,0,h_mm); seg(0,h_mm,0,0)
    return True

def load_fp(lib, mod):
    fp = pcbnew.FootprintLoad(lib, mod)
    if not fp:
        raise RuntimeError(f"FootprintLoad failed for {lib}:{mod}")
    return fp

def findfp(board, ref): return board.FindFootprintByReference(ref)

# ---------- mechanical ----------
def place_holes(board, holes):
    n=0
    for h in holes:
        dia = float(h["diameter"])
        lib = "MountingHole"; mod = f"MountingHole_{dia:.1f}mm" if abs(dia-3.2)>0.31 else "MountingHole_3.2mm_M3"
        fp = load_fp(lib, mod)
        fp.SetReference(f"H{n+1}")
        fp.SetPosition(pcbnew.VECTOR2I(MM(h["x"]), MM(h["y"])))
        board.Add(fp); n+=1
    return n

def add_keepout_rect(board, x,y,w,h, layers):
    rect = pcbnew.PCB_SHAPE(board); rect.SetShape(pcbnew.SHAPE_T_RECT)
    rect.SetLayer(pcbnew.F_Cu)
    rect.SetRect(pcbnew.EDA_RECT(pcbnew.VECTOR2I(MM(x),MM(y)), pcbnew.VECTOR2I(MM(x+w),MM(y+h))))
    ko = pcbnew.KEEPOUT_AREA(board); ko.SetBoundingBox(rect.GetRect())
    ls = pcbnew.LSET()
    for nm in layers:
        lid = board.GetLayerID(nm)
        if lid != pcbnew.UNDEFINED_LAYER: ls.AddLayer(lid)
    ko.SetLayerSet(ls); ko.SetDoNotAllowTracks(True); ko.SetDoNotAllowVias(True); ko.SetDoNotAllowCopperPour(True)
    board.Add(ko)

def keepout_around_holes(board, holes, radius_mm, layers):
    for i,h in enumerate(holes):
        x = h["x"]-radius_mm; y = h["y"]-radius_mm; d=2*radius_mm
        add_keepout_rect(board, x,y,d,d, layers)

# ---------- edge placements ----------
def edge_axis(board, edge, margin_mm=1.0):
    bb = board_bbox(board)
    if edge=="north":
        return ("h", bb.GetY()+MM(margin_mm), bb.GetX()+MM(margin_mm), bb.GetX()+bb.GetWidth()-MM(margin_mm))
    if edge=="south":
        return ("h", bb.GetY()+bb.GetHeight()-MM(margin_mm), bb.GetX()+MM(margin_mm), bb.GetX()+bb.GetWidth()-MM(margin_mm))
    if edge=="west":
        return ("v", bb.GetX()+MM(margin_mm), bb.GetY()+MM(margin_mm), bb.GetY()+bb.GetHeight()-MM(margin_mm))
    if edge=="east":
        return ("v", bb.GetX()+bb.GetWidth()-MM(margin_mm), bb.GetY()+MM(margin_mm), bb.GetY()+bb.GetHeight()-MM(margin_mm))
    raise RuntimeError(f"Unknown edge: {edge}")

def place_on_edge(board, ref, edge, offset_mm=0.0):
    fp = findfp(board, ref); if_not = (fp is None)
    if if_not: return False
    orient, f, a, b = edge_axis(board, edge, 1.0)
    if orient=="h":
        x = int((a+b)//2 + MM(offset_mm)); y=int(f)
        fp.SetPosition(pcbnew.VECTOR2I(x,y)); fp.SetOrientationDegrees(180.0 if edge=="north" else 0.0)
    else:
        y = int((a+b)//2 + MM(offset_mm)); x=int(f)
        fp.SetPosition(pcbnew.VECTOR2I(x,y)); fp.SetOrientationDegrees(90.0 if edge=="west" else -90.0)
    return True

def spread_on_edge(board, refs, edge, margin_mm=6.0):
    placed=0
    orient, f, a, b = edge_axis(board, edge, margin_mm)
    n=len(refs)
    for i,ref in enumerate(refs):
        fp = findfp(board, ref)
        if not fp: continue
        t=(i+1)/(n+1)
        if orient=="h":
            x=int(a+t*(b-a)); y=int(f)
            fp.SetPosition(pcbnew.VECTOR2I(x,y)); fp.SetOrientationDegrees(180.0 if edge=="north" else 0.0)
        else:
            y=int(a+t*(b-a)); x=int(f)
            fp.SetPosition(pcbnew.VECTOR2I(x,y)); fp.SetOrientationDegrees(90.0 if edge=="west" else -90.0)
        placed+=1
    return placed

def place_zone_center(board, refs, x,y,w,h, rot=0.0):
    cx=MM(x+w/2.0); cy=MM(y+h/2.0); n=0
    for ref in refs:
        fp = findfp(board, ref)
        if not fp: continue
        fp.SetPosition(pcbnew.VECTOR2I(int(cx),int(cy))); fp.SetOrientationDegrees(rot); n+=1
    return n

# ---------- decouplers ----------
def pad_list(fp):
    return [p for p in fp.Pads()]

def netname(pad): 
    n = pad.GetNet()
    return n.GetNetname() if n else ""

def collect_decouplers(board, cap_ident, gnd_name):
    caps=[]
    for fp in board.GetFootprints():
        if not fp.GetReference().upper().startswith(cap_ident.get("by_ref_prefix","C").upper()):
            continue
        pads = pad_list(fp)
        if len(pads)!=2: continue
        nets = [netname(p) for p in pads]
        if cap_ident.get("require_gnd", True) and gnd_name not in nets:
            continue
        caps.append(fp)
    return caps

def ic_power_nets(fp, keywords):
    nets=set()
    for p in pad_list(fp):
        nm = p.GetPadName().upper()
        if any(k in nm for k in keywords):
            nn = netname(p)
            if nn: nets.add(nn)
    # Also include nets connected to any pad named with +V or VDD etc
    for p in pad_list(fp):
        nn = netname(p)
        if nn and (nn.upper().startswith("V") or "3V3" in nn.upper() or "1V8" in nn.upper()):
            nets.add(nn)
    return list(nets)

def place_decouplers(board, ics, caps, gnd_name, max_dist_mm):
    placed=0
    # map caps by (power_net, gnd_name)
    cap_pairs=[]
    for c in caps:
        pads = pad_list(c)
        n1, n2 = netname(pads[0]), netname(pads[1])
        if n1==gnd_name and n2!=gnd_name:
            cap_pairs.append((c, pads[1], pads[0]))  # (cap, power_pad, gnd_pad)
        elif n2==gnd_name and n1!=gnd_name:
            cap_pairs.append((c, pads[0], pads[1]))
    for ic in ics:
        pwr_nets = set(ic_power_nets(ic, ["VDD","VCC","3V3","1V8","VIN","AVDD"]))
        if not pwr_nets: continue
        # pick one nearest cap per power net
        for (cap, pwr_pad, gnd_pad) in cap_pairs:
            if netname(pwr_pad) not in pwr_nets:
                continue
            # find IC pad with same power net
            target_pads = [p for p in pad_list(ic) if netname(p)==netname(pwr_pad)]
            if not target_pads: continue
            tpad = target_pads[0]
            tp = tpad.GetPosition()
            # place cap near the target pad with small offset towards board center
            offset = pcbnew.VECTOR2I(MM(max_dist_mm*0.6), 0)
            cap.SetPosition(tp + offset)
            cap.SetOrientationDegrees(0.0)
            placed+=1
    return placed

# ---------- via utilities ----------
def add_via(board, x_mm, y_mm, drill_mm, dia_mm, start=None, end=None, net=None):
    v = pcbnew.VIA(board)
    v.SetPosition(pcbnew.VECTOR2I(MM(x_mm),MM(y_mm)))
    v.SetDrill(MM(drill_mm)); v.SetWidth(MM(dia_mm))
    if start is None: start = pcbnew.F_Cu
    if end   is None: end   = pcbnew.B_Cu
    v.SetLayerPair(start, end)
    if net: v.SetNet(net)
    board.Add(v)
    return v

def via_ring(board, pitch_mm, inset_mm, drill_mm, dia_mm, net=None):
    bb = board_bbox(board)
    x0 = toMM(bb.GetX()); y0=toMM(bb.GetY()); w=toMM(bb.GetWidth()); h=toMM(bb.GetHeight())
    # Top & bottom edges
    x = x0 + inset_mm
    while x <= x0+w-inset_mm:
        add_via(board, x, y0+inset_mm, drill_mm, dia_mm, net=net)
        add_via(board, x, y0+h-inset_mm, drill_mm, dia_mm, net=net)
        x += pitch_mm
    # Left & right edges
    y = y0 + inset_mm
    while y <= y0+h-inset_mm:
        add_via(board, x0+inset_mm, y, drill_mm, dia_mm, net=net)
        add_via(board, x0+w-inset_mm, y, drill_mm, dia_mm, net=net)
        y += pitch_mm

def line_vias(board, x1,y1,x2,y2, pitch_mm, offset_mm, drill_mm, dia_mm, net=None):
    # place two parallel lines of vias offset +/- offset_mm from the corridor center line
    import math
    dx, dy = x2-x1, y2-y1
    L = math.hypot(dx,dy)
    if L < 1e-6: return
    ux, uy = dx/L, dy/L
    # normal
    nx, ny = -uy, ux
    # positions along the line
    npts = max(1, int(L / pitch_mm))
    for i in range(npts+1):
        t = i / npts
        cx = x1 + t*dx; cy = y1 + t*dy
        # upper/lower rails
        add_via(board, cx + nx*offset_mm, cy + ny*offset_mm, drill_mm, dia_mm, net=net)
        add_via(board, cx - nx*offset_mm, cy - ny*offset_mm, drill_mm, dia_mm, net=net)

# ---------- planes (simple rectangles) ----------
def rect_zone(board, net_name, layer_name, x,y,w,h, hatch_thickness=0.508):
    try:
        net = ensure_net(board, net_name)
        lid = board.GetLayerID(layer_name)
        if lid == pcbnew.UNDEFINED_LAYER: 
            return 0
        z = pcbnew.ZONE_CONTAINER(board)
        z.SetNetCode(net.GetNet()); z.SetLayer(lid)
        z.SetZoneClearance(MM(0.2))
        poly = z.Outline()
        poly.NewOutline()
        poly.Append(pcbnew.VECTOR2I(MM(x),MM(y)))
        poly.Append(pcbnew.VECTOR2I(MM(x+w),MM(y)))
        poly.Append(pcbnew.VECTOR2I(MM(x+w),MM(y+h)))
        poly.Append(pcbnew.VECTOR2I(MM(x),MM(y+h)))
        board.Add(z)
        z.Hatch()  # fill
        return 1
    except Exception:
        return 0

# ---------- netclasses ----------
def ensure_netclasses(board, classes_cfg):
    ds = board.GetDesignSettings()
    try:
        ncs = ds.GetNetClasses()
    except Exception:
        # older KiCad: access via board.GetDesignSettings().m_NetClasses?
        ncs = ds.GetNetClasses()
    for name, cfg in classes_cfg.items():
        try:
            nc = ncs.Find(name)
        except Exception:
            nc = None
        if not nc:
            nc = pcbnew.NETCLASS(name)
            ncs.Add(nc)
        # set widths/clearances
        if "width_mm" in cfg:
            nc.SetTrackWidth(MM(cfg["width_mm"]))
        if "clear_mm" in cfg:
            nc.SetClearance(MM(cfg["clear_mm"]))
        # differential
        if "diff_gap_mm" in cfg:
            try: nc.SetDiffPairGap(MM(cfg["diff_gap_mm"]))
            except Exception: pass
        if "diff_width_mm" in cfg:
            try: nc.SetDiffPairWidth(MM(cfg["diff_width_mm"]))
            except Exception: pass
        # assign nets
        for netname in cfg.get("nets", []):
            try: nc.AddNet(netname)
            except Exception: pass

# ---------- thermal via grids ----------
def thermal_via_grid(board, refs, pitch_mm, rows, cols, drill_mm, dia_mm):
    added=0
    for ref in refs:
        fp = findfp(board, ref)
        if not fp: continue
        bb = fp.GetFootprintRect()
        x0 = toMM(bb.GetX()); y0 = toMM(bb.GetY())
        w  = toMM(bb.GetWidth()); h = toMM(bb.GetHeight())
        cx = x0 + w/2.0; cy = y0 + h/2.0
        sx = (cols-1)*pitch_mm; sy = (rows-1)*pitch_mm
        for r in range(rows):
            for c in range(cols):
                x = cx - sx/2.0 + c*pitch_mm
                y = cy - sy/2.0 + r*pitch_mm
                add_via(board, x,y, drill_mm, dia_mm, net=None)
                added+=1
    return added

# ---------- testpoints ----------
def add_testpoints(board, tp_footprint, nets):
    added=0
    # try to place near the first pad of each net we find
    for netname in nets:
        ni = ensure_net(board, netname)
        # find any pad on that net
        padpos=None
        for fp in board.GetFootprints():
            for p in fp.Pads():
                if p.GetNet() and p.GetNet().GetNetname()==netname:
                    padpos = p.GetPosition(); break
            if padpos: break
        if not padpos: continue
        lib, mod = tp_footprint.split(":")
        tp = load_fp(lib, mod)
        tp.SetReference(f"TP{added+1}")
        # offset 1.2 mm right
        tp.SetPosition(padpos + pcbnew.VECTOR2I(MM(1.2), 0))
        board.Add(tp); added+=1
    return added

# ---------- SPI guard corridor ----------
def zone_center(cfg_zone):
    return (cfg_zone["x"]+cfg_zone["w"]/2.0, cfg_zone["y"]+cfg_zone["h"]/2.0)

class K1ContractedPlacePRO(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "K1: Contracted Place PRO"
        self.category = "K1 Tools"
        self.description = "Apply design contract v2: outline, holes, keepouts, placements, decouplers, via fences, netclasses, planes, thermals, testpoints"
        self.show_toolbar_button = True
        self.icon_file_name = ""

    def Run(self):
        try:
            board = pcbnew.GetBoard()
            bp = board.GetFileName()
            root = repo_root_from(bp, "tools/k1_project_v2.json")
            cfg = read_json(os.path.join(root,"tools/k1_project_v2.json"))

            # Outline
            mech = cfg["mechanical"]
            added_outline = add_edge_rect(board, mech["outline"]["width"], mech["outline"]["height"])
            # Holes + keepouts
            holes = mech.get("mounting_holes", [])
            n_holes = place_holes(board, holes) if holes else 0
            # Keepouts: antenna etc
            for ko in mech.get("keepouts", []):
                add_keepout_rect(board, ko["x"], ko["y"], ko["w"], ko["h"], ko.get("layers",["F.Cu","B.Cu"]))
            # Keepout rings around holes
            keepout_layers = ["F.Cu","B.Cu","F.Mask","B.Mask"]
            for h in holes:
                rad = float(h.get("keepout",0))/2.0
                if rad>0: add_keepout_rect(board, h["x"]-rad, h["y"]-rad, 2*rad, 2*rad, keepout_layers)

            # Edge placements
            io = cfg.get("io",{})
            if io.get("usb") and io["usb"].get("ref"):
                place_on_edge(board, io["usb"]["ref"], io["usb"].get("edge","south"), io["usb"].get("offset_mm",0.0))
            placed_leds = 0
            if io.get("led_ports") and io["led_ports"].get("refs"):
                placed_leds = spread_on_edge(board, io["led_ports"]["refs"], io["led_ports"].get("edge","north"), io["led_ports"].get("margin_mm",6.0))

            # Zone placements for COM_A/COM_B
            zoned=0
            for z in cfg.get("placement_zones", []):
                zoned += place_zone_center(board, z.get("refs",[]), z["x"], z["y"], z["w"], z["h"], z.get("rotation",0.0))

            # Netclasses
            ensure_netclasses(board, cfg.get("routing",{}).get("netclasses", {}))

            # Decouplers near IC power pins
            gnd = ensure_net(board, cfg["power_nets"]["gnd"])
            caps = collect_decouplers(board, cfg["decoupling"]["cap_ident"], gnd.GetNetname())
            ics  = [fp for fp in board.GetFootprints() if fp.GetReference().startswith("U")]
            dec_placed = place_decouplers(board, ics, caps, gnd.GetNetname(), cfg["decoupling"]["max_distance_mm"])

            # Edge GND via ring
            ring = mech.get("edge_via_ring", {"enabled": False})
            if ring.get("enabled", False):
                via_ring(board, ring.get("pitch_mm",3.0), ring.get("inset_mm",0.8),
                         ring["via"].get("drill_mm",0.3), ring["via"].get("dia_mm",0.6), net=gnd)

            # SPI guard corridor between COM_A and COM_B
            spi_guard = cfg.get("routing",{}).get("spi",{}).get("guard",{"enabled":False})
            if spi_guard.get("enabled", False) and len(cfg.get("placement_zones",[]))>=2:
                zA = cfg["placement_zones"][0]; zB = cfg["placement_zones"][1]
                ax, ay = zone_center(zA); bx, by = zone_center(zB)
                line_vias(board, ax, ay, bx, by,
                          spi_guard.get("pitch_mm",2.0),
                          spi_guard.get("offset_mm",1.2),
                          spi_guard["via"].get("drill_mm",0.3),
                          spi_guard["via"].get("dia_mm",0.6),
                          net=gnd)

            # Power planes (basic rectangles)
            planes = cfg.get("planes", {})
            # GND plane: whole board minus margin (expand_mm < 0 shrinks)
            gp = planes.get("gnd")
            if gp:
                bb = board_bbox(board)
                x = toMM(bb.GetX()); y = toMM(bb.GetY()); w=toMM(bb.GetWidth()); h=toMM(bb.GetHeight())
                expand = float(gp.get("expand_mm",-0.2"))
                rect_zone(board, cfg["power_nets"]["gnd"], gp.get("layer","In1.Cu"),
                          x - expand, y - expand, w + 2*expand, h + 2*expand)
            # Power islands
            for isl in planes.get("power_islands", []):
                r = isl["rect"]
                rect_zone(board, isl["net"], isl["layer"], r["x"], r["y"], r["w"], r["h"])

            # Thermal via grids under hot parts
            therm = cfg.get("thermal",{}).get("hot_parts",[])
            therm_added = 0
            for hp in therm:
                vg = hp.get("via_grid",{})
                therm_added += thermal_via_grid(board, hp.get("refs",[]), vg.get("pitch_mm",1.2),
                                                vg.get("rows",2), vg.get("cols",3),
                                                vg.get("via",{}).get("drill_mm",0.3),
                                                vg.get("via",{}).get("dia_mm",0.6))

            # Testpoints
            tp_cfg = cfg.get("testpoints",{})
            tps = 0
            if tp_cfg.get("nets"):
                tps = add_testpoints(board, tp_cfg.get("footprint","TestPoint:TestPoint_Pad_D1.00mm"), tp_cfg["nets"])

            board.BuildListOfNets()
            board.Save(bp)

            wx.MessageBox(
                "Contract PRO applied.\n"
                f"Outline new: {added_outline}\n"
                f"Mounting holes: {n_holes}\n"
                f"LED ports placed: {placed_leds}\n"
                f"Zoned refs: {zoned}\n"
                f"Decouplers placed: {dec_placed}\n"
                f"Thermal vias: {therm_added}\n"
                f"Testpoints: {tps}\n",
                "K1: Contracted Place PRO"
            )
        except Exception as e:
            wx.MessageBox(f"ERROR: {e}", "K1: Contracted Place PRO", style=wx.ICON_ERROR)

K1ContractedPlacePRO().register()
