"""
    Misc helpers
"""
from py_stealth import *

def cancel_targets():
    """
        Cancel target and wait target
    """
    if TargetPresent():
        CancelTarget()
    CancelWaitTarget()

def get_context_menu_entry_id(item_id: int, entry: str) -> int:
    """Get context menu entry id by item id and entry text

    Args:
        item_id (int): Item ID
        entry (str): Entry text

    Returns:
        int: Entry ID
    """

    attempt = 0
    SetContextMenuHook(0, 0)
    ClearContextMenu()

    while not GetContextMenu() and attempt < 10:
        RequestContextMenu(item_id)
        Wait(1000)
        attempt += 1

    for menu_entry in GetContextMenu():
        entry_id, _, entry_text, _, _ = menu_entry.split("|")
        if not entry_text:
            continue
        if entry_text == entry:
            return entry_id

    SetContextMenuHook(0, 0)
    ClearContextMenu()

    return -1

def open_container(container: int) -> bool:
    """Tries to open container. If attempts > 10 - fails.

    Returns:
        bool: True if container was opened
    """

    attempt = 0
    while LastContainer() != Backpack():
        UseObject(Backpack())
        Wait(1000)

    while LastContainer() != container:
        attempt += 1
        if attempt >= 10:
            return False
        UseObject(container)
        Wait(1000)

    return LastContainer() == container
