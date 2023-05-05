from .types import Types
from .gump import Gump
from py_stealth import *


class Runebook(Gump):
    """
        Class for tile manipulation
    """

    def __init__(self) -> None:
        self.open()
        self._params = Types().find_by_name("runebook")
        super().__init__(self._params["id"])
        self.to_title_screen()

    def open(self) -> None:
        """
            Open runebook
        """
        self._close_all()
        gump_count = GetGumpsCount()
        while gump_count == GetGumpsCount():
            print(f"Try {gump_count=} {GetGumpsCount()=}")
            UOSay("[runebook")
            Wait(500)

    def to_title_screen(self) -> None:
        if buttons:= self._find_buttons_by_graphic(self._params["nav_back_button_graphic"]):
            self._press_button(buttons[0]["value"], True)


    def recall(self, route: list):
        x, y = GetX(Self()), GetY(Self())

        self.open()
        self.to_title_screen()


        for entry in route:
            print(f"Route to {entry}")

            for button in self._find_buttons_row_by_text(entry):
                if button["graphic"] == self._params["recall_button_graphic"]:
                    self._press_button(button["value"])
                    if entry == route[-1]:
                        print("Last point reached")
                        Wait(1000)
                        if [x, y] == [GetX(Self()), GetY(Self())]:
                            print("Recall failed")

