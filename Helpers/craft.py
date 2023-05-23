from Scripts.Config.types import Types
from .gump import Gump
from py_stealth import *


class Craft(Gump):
    """
        Class for tile manipulation
    """

    def __init__(self, tool: int) -> None:
        self._tool = tool
        self.open()
        self._params = Types().find_by_name("crafting")
        super().__init__(self._params["id"])

    def open(self) -> None:
        """
            Open runebook
        """
        if not FindType(self._tool, Backpack()):
            raise ValueError(f"Tool {hex(self._tool)} not found in backpack")

        self._close_all()
        gump_count = GetGumpsCount()
        while gump_count == GetGumpsCount():
            # TODO: Logger -> Debug
            # print(f"Try {gump_count=} {GetGumpsCount()=}")
            UseType(self._tool, 0xFFFF)
            Wait(500)

    def craft(self, route: list):
        self.open()
        # TODO: Logger -> Debug
        # print(f"Crafting {'->'.join(route)}")
        for entry in route:
            for button in self._find_buttons_row_by_text(entry):
                if button["graphic"] == self._params["craft_button_graphic"]:
                    self._press_button(button["value"])
