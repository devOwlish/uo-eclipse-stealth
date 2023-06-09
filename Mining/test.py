"""
    Mining script.
    Prerequisites:
        - Mining category in the runebook
            - Recall points for unload and mining

        - At least one tinker's tool in the backpack
        - House
"""


from datetime import datetime as dt, timedelta
from py_stealth import *
from Scripts.Config.tiles import Tiles
from Scripts.Config.types import Types
from Scripts.Helpers.logger import Logger
from Scripts.Helpers.runebook import Runebook
from Scripts.Helpers.craft import Craft
from Scripts.Helpers.misc import (
    cancel_targets,
    get_context_menu_entry_id,
    open_container
)


# TODO: Logger
class Miner():
    """
        Miner bot
    """
    def __init__(self, resource: str = "ore") -> None:
        self._types = Types()
        self._pickaxe = self._types.find_by_name("pickaxe")
        self._forge = self._types.find_by_name("forge")
        self._ores = self._types.find_by_name("ores")
        self._resources = self._ores + \
            self._types.find_by_name("granite") + \
            self._types.find_by_name("mining_gems") + [0x14F0]
        self._ingots = self._types.find_by_name("ingots")[0]

        self._logger = Logger().get()
        # TODO: Change
        self._unload_box = 0x4299F0C3
        self._gatherer = 0x00002A66
        self._order_claimed_dt = dt.now()


        self._runebook = Runebook()
        self._crafting = Craft(self._types.find_by_name("tinker_tools"))

        ClearSystemJournal()
        SetARStatus(True)
        SetPauseScriptOnDisconnectStatus(True)
        SetWarMode(False)
        SetFindDistance(20)

        # Set mining type
        # We need at least 1 pickaxe to set the mining type
        self._handle_tools()
        if FindType(self._pickaxe, Backpack()):
            entry_id = get_context_menu_entry_id(FindItem(), f"Set to {resource.capitalize()}")
            if entry_id == -1:
                print(f"Failed to get context menu entry id for {resource.capitalize()}")
                exit()
            SetContextMenuHook(FindItem(), entry_id)
            SetContextMenuHook(0, 0)
        else:
            self._logger.critical("No pickaxe found, exiting")
            exit()

    # TODO: To base class?
    def run(self):
        """
            Main loop
        """
        self._runebook.recall(["Mining", "Mine"])
        while not Dead():
            tiles = Tiles("cave")
            tiles.find_around(10)
            for _ in range(len(tiles.get_tiles())):
                self._mine(tiles.pop_closest_tile())

    # TODO: To base class?
    def _unstuck(self) -> None:
        """
            If there is overload, we can't recall. Thus, we must drop some ore.
        """
        # The idea is to avoid "You are already there" message
        newMoveXY(GetX(Self())+1, GetY(Self()), True, 1, True)
        to_drop = [0x0000, 0xFFFF]

        for color in to_drop:
            # We're free to go
            if Weight() < MaxWeight():
                return

            print(f"Unstuck: Dropping {hex(color)}")
            if FindTypesArrayEx(self._resources, [color], [Backpack()], False):
                MoveItem(FindItem(), 10,  Ground(), GetX(Self()) + 1, GetY(Self()), GetZ(Self()))
                Wait(1000)
                print("Dropped")
                return

    def _smelt(self):
        """
            Smelt ores
        """
        self._runebook.recall(["Mining", "Smelt"])

        if FindType(self._forge, Ground()):
            forge = FindItem()
            newMoveXY(GetX(forge), GetY(forge), True, 1, True)
            if FindTypesArrayEx(self._ores, [0xFFFF], [Backpack()], False):
                ores = GetFindedList()
                for ore in ores:
                    WaitTargetObject(forge)
                    UseObject(ore)
                    WaitJournalLine(dt.now(), "|".join(
                        ["You smelt", "You burn", "not enough", "Someone has gotten"]), 15000)

        self._runebook.recall(["Mining", "Mine"])

    # TODO: To base class?
    def _unload(self):
        self._unstuck()
        if not self._runebook.recall(["Mining", "Unload"]):
            print("Recall to unload failed")
            return

        if FindTypesArrayEx(self._resources, [0xFFFF], [Backpack()], False):
            for ore in GetFoundList():
                MoveItem(ore, -1, self._unload_box, 0, 0, 0)
                Wait(1000)

        if not FindTypeEx(self._ingots, 0x0000, Backpack()) or FindQuantity() < 100:
            print("Need to restock")
            open_container(self._unload_box)
            if FindTypeEx(self._ingots, 0x0000, self._unload_box) and FindQuantity() > 100:
                MoveItem(FindItem(), 100, Backpack(), 0, 0, 0)
                Wait(1000)
            else:
                print("No ingots found in the unload box")
                exit()

        if not self._runebook.recall(["Mining", "Mine"]):
            print("Recall to mine failed")
            return

    def _claim_order(self):
        time_diff = self._order_claimed_dt - dt.now()

        if time_diff.total_seconds() / 60 > -31:
            return

        self._order_claimed_dt = dt.now()

        if not self._runebook.recall(["Mining", "Gatherer"]):
            print("Recall to gatherer failed")
            return

        if IsObjectExists(self._gatherer):
            entry_id = get_context_menu_entry_id(self._gatherer, "Talk")
            if entry_id == -1:
                print("Failed to get context menu entry id for 'Talk'")
            SetContextMenuHook(self._gatherer, entry_id)
            SetContextMenuHook(0, 0)
            Wait(1000)
        else:
            self._logger.critical("No Gatherer NPC found")


        if not self._runebook.recall(["Mining", "Mine"]):
            print("Recall to mine failed")
            return

    # TODO: To base class?
    def _handle_tools(self):
        if Count(self._pickaxe) < 2:
            self._crafting.craft(["Tools", "pickaxe"])

        if Count(self._types.find_by_name("tinker_tools")) < 2:
            self._crafting.craft(["Tools", "tinker's tools"])

    # TODO: To base class?
    # TODO: Abstract harvest method ?
    def _mine(self, tile):
        tile, x, y, z = tile
        while not Dead():
            if Weight() >= MaxWeight() - 50:
                if Weight() > MaxWeight():
                    self._unstuck()
                self._unload()
            self._claim_order()
            if newMoveXY(x, y, True, 1, True):
                started = dt.now()
                cancel_targets()
                self._handle_tools()

                if FindType(self._pickaxe, Backpack()):
                    UseObject(FindItem())
                    WaitForTarget(2000)

                if TargetPresent():
                    TargetToTile(tile, x, y, z)
                    # WaitTargetTile(tile, x, y, z)
                    # TODO: To messages
                    WaitJournalLine(started, "|".join(
                        ["You dig", "workable stone", "You loosen", "There is no", "too far"]), 15000)

                # TODO: To messages
                if InJournalBetweenTimes("|".join(["There is no", "too far"]), started, dt.now()) > 0:
                    break
            else:
                print(f"Can't reach X: {x} Y: {y}")
                # Recall failed? Let's try one more time
                self._runebook.recall(["Mining", "Mine"])


if __name__ == "__main__":
    ClearSystemJournal()

    miner = Miner(
        "stone"
    )
    miner.run()