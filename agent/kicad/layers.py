"""
LSET/LSEQ helpers for KiCad PCBnew.

This module wraps the SWIG-exposed pcbnew.LSET and pcbnew.LSEQ to avoid
common misuse patterns:
  - NEVER pass strings (e.g., "F.Cu") directly to LSET constructor
  - NEVER pass raw ints without mapping to PCB_LAYER_ID enums
  - ALWAYS use PCB_LAYER_ID enum constants (e.g., pcbnew.F_Cu)
  - Use .AddLayer(id) or initializer list with enums for safety

Reference: SWIG bindings accept only:
  - LSET()
  - LSET(BASE_SET)
  - LSET({PCB_LAYER_ID, ...})  (initializer list, enums only)
  - LSET(std::vector<PCB_LAYER_ID>)
  - LSET(LSEQ)
  - LSET(LAYER_RANGE)
"""

import pcbnew


def lset(*layer_ids: int) -> pcbnew.LSET:
    """
    Create an LSET from one or more PCB_LAYER_ID enum constants.

    Args:
        *layer_ids: PCB_LAYER_ID enum values (e.g., pcbnew.F_Cu, pcbnew.B_Cu)

    Returns:
        pcbnew.LSET: A layer set object

    Example:
        cu_layers = lset(pcbnew.F_Cu, pcbnew.In1_Cu, pcbnew.B_Cu)
        zone.SetLayerSet(cu_layers)

    Raises:
        RuntimeError: If any layer_id is not a valid PCB_LAYER_ID
    """
    s = pcbnew.LSET()
    for lid in layer_ids:
        # Validate: layer_ids should be PCB_LAYER_ID enums (int range)
        if not isinstance(lid, int) or lid < 0 or lid >= pcbnew.PCB_LAYER_ID_COUNT:
            raise RuntimeError(
                f"Invalid layer ID {lid}. Must be PCB_LAYER_ID enum (e.g., pcbnew.F_Cu)"
            )
        s.AddLayer(lid)
    return s


def lset_from_names(board: pcbnew.BOARD, *names: str) -> pcbnew.LSET:
    """
    Create an LSET from layer name strings, mapping via board.GetLayerID().

    This is safe for string layer names like "F.Cu", "B.Cu", "In1.Cu".
    The board's GetLayerID() method handles the string→PCB_LAYER_ID conversion.

    Args:
        board: pcbnew.BOARD object (source of truth for layer IDs)
        *names: Layer name strings (e.g., "F.Cu", "B.Cu", "In1.Cu")

    Returns:
        pcbnew.LSET: A layer set object

    Example:
        cu_layers = lset_from_names(board, "F.Cu", "B.Cu")
        zone.SetLayerSet(cu_layers)

    Raises:
        RuntimeError: If any layer name is unknown to the board
    """
    s = pcbnew.LSET()
    for nm in names:
        lid = board.GetLayerID(nm)
        if lid == pcbnew.UNDEFINED_LAYER:
            raise RuntimeError(
                f"Unknown layer: '{nm}'. Check board layer names (F.Cu, B.Cu, In1.Cu, etc.)"
            )
        s.AddLayer(lid)
    return s


def all_cu_layers() -> pcbnew.LSET:
    """
    Create an LSET containing all copper layers (F.Cu through B.Cu).

    This is a convenience for designs that use all available copper layers.
    The actual number of layers is determined by KiCad's PCB_LAYER_ID range.

    Returns:
        pcbnew.LSET: Layer set with F.Cu, In1_Cu, In2_Cu, ..., B.Cu

    Example:
        all_cu = all_cu_layers()
        via_class.SetLayerSet(all_cu)
    """
    s = pcbnew.LSET()
    # F_Cu is the first copper layer; B_Cu is the last
    # Iterate through all valid copper layer IDs
    for lid in range(pcbnew.F_Cu, pcbnew.B_Cu + 1):
        s.AddLayer(lid)
    return s


def lseq_from_lset(lset_obj: pcbnew.LSET) -> pcbnew.LSEQ:
    """
    Convert an LSET to an LSEQ (layer sequence).

    LSEQ is an ordered sequence (typically in physical order from front to back).
    This is useful when you need a deterministic iteration order.

    Args:
        lset_obj: pcbnew.LSET to convert

    Returns:
        pcbnew.LSEQ: An ordered sequence of layers

    Example:
        cu_set = lset(pcbnew.F_Cu, pcbnew.B_Cu)
        seq = lseq_from_lset(cu_set)
        for layer_id in seq:
            print(f"Layer: {layer_id}")
    """
    # LSEQ constructor accepts LSET
    return pcbnew.LSEQ(lset_obj)


def layer_name(board: pcbnew.BOARD, layer_id: int) -> str:
    """
    Get the human-readable name of a layer given its ID.

    Args:
        board: pcbnew.BOARD object
        layer_id: PCB_LAYER_ID enum value

    Returns:
        str: Layer name (e.g., "F.Cu", "B.Cu", "F.SilkS")

    Example:
        name = layer_name(board, pcbnew.F_Cu)  # "F.Cu"
    """
    return board.GetLayerName(layer_id)


def is_copper_layer(layer_id: int) -> bool:
    """
    Check if a layer ID is a copper layer.

    Args:
        layer_id: PCB_LAYER_ID enum value

    Returns:
        bool: True if the layer is copper (F.Cu through B.Cu), False otherwise
    """
    return pcbnew.F_Cu <= layer_id <= pcbnew.B_Cu


def is_mask_layer(layer_id: int) -> bool:
    """
    Check if a layer ID is a solder mask layer.

    Args:
        layer_id: PCB_LAYER_ID enum value

    Returns:
        bool: True if the layer is mask (F.Mask or B.Mask)
    """
    return layer_id in (pcbnew.F_Mask, pcbnew.B_Mask)


def is_silk_layer(layer_id: int) -> bool:
    """
    Check if a layer ID is a silkscreen layer.

    Args:
        layer_id: PCB_LAYER_ID enum value

    Returns:
        bool: True if the layer is silkscreen (F.SilkS or B.SilkS)
    """
    return layer_id in (pcbnew.F_SilkS, pcbnew.B_SilkS)
