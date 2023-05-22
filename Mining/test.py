"""
    Mining script.
    Prerequisites:
        - Mining category in the runebook
            - Recall points for unload and mining

        - At least one tinker's tool in the backpack
        - House
"""

# TODO: Get some ingots from the unload chest
# TODO: Don't hardcode shit, pass it or smth
# TODO: Variability? Whether it's worths


from datetime import datetime as dt
from py_stealth import *
from Scripts.Helpers.tiles import Tiles
from Scripts.Helpers.types import Types
from Scripts.Helpers.runebook import Runebook
from Scripts.Helpers.craft import Craft
from Scripts.Helpers.misc import cancel_targets

STATE_IDLE = "IDLE"
STATE_OVERLOADED = "OVERLOADED"


# TODO: Logger
class Miner():
    """
        Miner bot
    """
    def __init__(self, runebook: Runebook, crafting: Craft) -> None:
        self._state = STATE_IDLE
        self._pickaxe = Types().find_by_name("pickaxe")
        self._forge = Types().find_by_name("forge")
        self._ores = Types().find_by_name("ores")
        self._gems = Types().find_by_name("mining_gems")
        self._runebook = runebook
        self._crafting = crafting

        ClearSystemJournal()
        SetFindDistance(20)

    # TODO: To base class?
    def run(self):
        self._runebook.recall(["Mining", "Mine"])
        # TODO: Revision
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
        # TODO: Make it more sane
        # The idea is to avoid "You are already there" message
        newMoveXY(GetX(Self())+1, GetY(Self()), True, 1, True)
        to_drop = [0x0000, 0xFFFF]

        for color in to_drop:
            # We're free to go
            if Weight() < MaxWeight():
                return

            print(f"Unstuck: Dropping {hex(color)}")
            if FindTypesArrayEx(self._ores, [color], [Backpack()], False):
                MoveItem(FindItem(), 10,  Ground(), GetX(Self()) + 1, GetY(Self()), GetZ(Self()))
                Wait(1000)
                # TODO: Make some sane shit out of it
                print("Dropped")
                return

    def _smelt(self):
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

        if FindTypesArrayEx(self._ores + self._gems, [0xFFFF], [Backpack()], False):
            for ore in GetFoundList():
                MoveItem(ore, -1, 0x4299F0C3, 0, 0, 0)
                Wait(1000)

        if not self._runebook.recall(["Mining", "Mine"]):
            print("Recall to mine failed")
            return

    # TODO: To base class?
    def _handle_tools(self):
        # TODO: Get some ingots ffs
        if Count(self._pickaxe) < 2:
            self._crafting.craft(["Tools", "pickaxe"])

        if Count(Types().find_by_name("tinker_tools")) < 2:
            self._crafting.craft(["Tools", "tinker's tools"])

    # TODO: To base class?
    # TODO: Abstract harvest method ?
    def _mine(self, tile):
        tile, x, y, z = tile
        while not Dead():
            if Weight() > MaxWeight():
                self._unstuck()

            if Weight() >= MaxWeight() - 50:
                self._unload()

            if newMoveXY(x, y, True, 1, True):
                started = dt.now()
                cancel_targets()
                self._handle_tools()

                if FindType(self._pickaxe, Backpack()):
                    UseType(self._pickaxe, 0xFFFF)
                    WaitForTarget(2000)

                if TargetPresent():
                    WaitTargetTile(tile, x, y, z)
                    # TODO: To messages
                    WaitJournalLine(started, "|".join(
                        ["You dig", "You loosen", "There is no"]), 15000)

                # TODO: To messages
                if InJournalBetweenTimes("|".join(["There is no", "iron", "too far"]), started, dt.now()) > 0:
                    break
            else:
                # TODO: Critical
                print(f"Can't reach X: {x} Y: {y}")
                # Recall failed? Let's try one more time TODO: Revision
                self._runebook.recall(["Mining", "Mine"])


if __name__ == "__main__":
    ClearSystemJournal()

    miner = Miner(
        Runebook(), Craft(Types().find_by_name("tinker_tools"))
    )
    miner.run()


    # rb = Runebook()

    # rb.recall([
    #     "Trammel", "Britain"
    # ])

    # rb.recall([
    #     "Common", "Home"
    # ])
