# K1_ExportDSN.py
# Action Plugin: Export board to Specctra DSN format for FreeRouting
#
# Runs inside KiCad where pcbnew/wx are valid

import pcbnew
import wx
import os
import json

class K1ExportDSN(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "K1: Export to DSN"
        self.category = "K1 Tools"
        self.description = "Export board to Specctra DSN format for FreeRouting"
        self.show_toolbar_button = True
        self.icon_file_name = ""

    def _load_config(self, board_path):
        import json
        proj_dir = os.path.abspath(os.path.join(board_path, os.pardir, os.pardir)) \
                   if board_path.endswith(".kicad_pcb") else os.getcwd()
        cfg_path = os.path.join(proj_dir, "tools", "k1_config.json")
        if not os.path.exists(cfg_path):
            raise RuntimeError(f"Config file not found: {cfg_path}")
        with open(cfg_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def Run(self):
        try:
            board = pcbnew.GetBoard()
            board_path = board.GetFileName()
            cfg = self._load_config(board_path)
            output_dsn = cfg["dsn_path"]

            # Export to Specctra DSN format
            pcbnew.ExportSpecctraDSN(output_dsn, board)

            wx.MessageBox(
                f"DSN exported successfully to:\n{output_dsn}",
                "K1 Export DSN",
                style=wx.ICON_INFORMATION
            )
        except Exception as e:
            wx.MessageBox(
                f"ERROR: {str(e)}",
                "K1 Export DSN",
                style=wx.ICON_ERROR
            )

K1ExportDSN().register()
