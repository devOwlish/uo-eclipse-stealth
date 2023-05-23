from py_stealth import *


class Gump():
    """
    Class for gump manipulation
    """

    def __init__(self, gump_id: int) -> None:
        self._id = gump_id
        self._serial = self._find_id()
        self._index = self._find_index()
        self._clilocs = {}
        # TODO: Logger -> Debug
        # print(f"Gump serial: {hex(self._serial)=}")

    @staticmethod
    def _close_all():
        """
        Closes all gumps that can be closed by CloseSimpleGump
        """
        attempt = 0
        while GetGumpsCount() > 0 and attempt < 10:
            for index in range(0, GetGumpsCount()):
                CloseSimpleGump(index)
                NumGumpButton(index, 0)
                Wait(500)
            Wait(100)

            attempt += 1

    def _find_id(self) -> int:
        """Finds gump id by gump serial

        Raises:
            ValueError: If gump was not found

        Returns:
            int: Gump id
        """

        for index in range(0, GetGumpsCount()):
            if GetGumpID(index) == self._id:
                return GetGumpSerial(index)

        raise ValueError(f"Gump with id {hex(self._id)} was not found")

    def _find_index(self) -> int:
        """Finds gump index by gump id

        Raises:
            ValueError: If gump was not found

        Returns:
            int: Gump index
        """

        for index in range(0, GetGumpsCount()):
            if GetGumpID(index) == self._id:
                return index

        raise ValueError(f"Gump with id {hex(self._id)} was not found")

    def _press_button(self, button: int, wait: bool = False) -> None:
        """Presses button on the gump

        Args:
            button (int): Button ID
            wait (bool, optional): If True, wait for the next gump to appear. Defaults to False.
        """

        NumGumpButton(self._index, button)
        Wait(500)
        if wait:
            self._wait_for_gump()

    def _wait_for_gump(self) -> bool:
        """Waits for gump to appear

        Returns:
            bool: True if gump was found, False otherwise
        """

        attempt = 0

        while attempt < 10:
            try:
                self._find_index()
                return True
            except ValueError:
                Wait(500)
                attempt += 1

        return False

    def _find_buttons_by_graphic(self, graphic: int) -> list:
        """Finds all buttons with the passed graphic

        Args:
            graphic (int): Graphic to search for

        Returns:
            list: List of buttons
        """

        return [{
            "value": button["ReturnValue"],
            "x": button["X"],
            "y": button["Y"],
            "graphic": button["ReleasedID"]}
            for button in GetGumpInfo(self._index)["GumpButtons"] if button["ReleasedID"] == graphic]


    def _get_cliloc_by_id(self, cliloc_id: int) -> str:
        """Gets cliloc by id and caches it.

        Args:
            cliloc_id (int): Cliloc id

        Returns:
            str: Cliloc text
        """

        if cliloc_id in self._clilocs:
            return self._clilocs[cliloc_id]

        text = GetClilocByID(cliloc_id)
        self._clilocs[cliloc_id] = text

        return text

    def _parse_gump_text(self, gump_info: str, filter: str = "") -> list[dict[str, int, int, int]]:
        """
        Parses gump text, returns list of dicts with text, x, y and page;
        two sources are supported: XmfHTMLGumpColor and CroppedText

        Args:
            gump_info (str): Gump info
            filter (str, optional): Filter, all non-mathing lines are excluded from the output. Defaults to "".

        Returns:
            list[dict]: List of dicts with text, x, y and page
        """
        result = []

        # Parse from XmfHTMLGumpColor
        for gump_text in gump_info["XmfHTMLGumpColor"]:
            text = self._get_cliloc_by_id(gump_text["ClilocID"])

            if filter and not filter in text:
                continue

            result.append({
                "text": GetClilocByID(gump_text["ClilocID"]),
                "x": gump_text["X"],
                "y": gump_text["Y"],
                "page": gump_text["Page"],
            })

        # Parse from CroppedText
        flatten_text = [item for sublist in gump_info["Text"]
                        for item in sublist]

        for gump_text in gump_info["CroppedText"]:
            if gump_text["TextID"] in range(len(flatten_text)):
                text = flatten_text[gump_text["TextID"]]

                if filter and not filter in text:
                    continue

                result.append({
                    "text": text,
                    "x": gump_text["X"],
                    "y": gump_text["Y"],
                    "page": gump_text["Page"],
                })
            else:
                # TODO: Debug
                print(f"Failed to parse text {gump_text}")

        return result



    def _find_buttons_row_by_text(self, text: str, precision: int = 3) -> list[dict[int, int, int, int]]:
        """Finds all buttons in the same row as text

        Args:
            text (str): Text to search for
            precision (int, optional): Y coordinate precision . Defaults to 3.

        Returns:
            list: _description_
        """
        buttons = []

        gump_info = GetGumpInfo(self._index)

        texts = self._parse_gump_text(gump_info, text)

        for entry in texts:
            for button in gump_info["GumpButtons"]:
                if button["Y"] in range(entry["y"] - precision, entry["y"] + precision) and button["Page"] == entry["page"]:
                    buttons.append({
                        "value": button["ReturnValue"],
                        "x": button["X"],
                        "y": button["Y"],
                        "graphic": button["ReleasedID"]
                    })

        return buttons
