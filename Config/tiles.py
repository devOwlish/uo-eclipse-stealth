from .config import Config
from py_stealth import *
from math import sqrt


class Tiles():
    """
        Class for tile manipulation
    """
    def __init__(self, tile_type: str) -> None:
        self._tile_types = Config("common/tiles.yaml").get_by_key(tile_type)
        self._tiles = []

    def find_around(self, radius: int = 15) -> None:
        """ Find tiles around the player

        Args:
            radius (int, optional): Search radius. Defaults to 15.
        """

        min_x, min_y = GetX(Self())-radius, GetY(Self())-radius
        max_x, max_y = GetX(Self())+radius, GetY(Self())+radius

        for tile_type in self._tile_types:
            self._tiles += GetStaticTilesArray(
                min_x, min_y, max_x, max_y, WorldNum(), tile_type)

    def sort_tiles(self) -> None:
        """
            Sort tiles by distance to the player
        """

        player = [GetX(Self()), GetY(Self())]

        self._tiles = sorted(
            self._tiles,
            key=lambda tile: self._distance(
                [tile[1], tile[2]], player
            )
        )

    def get_tiles(self) -> list:
        """
            Returns tiles
        """
        return self._tiles

    def get_closest_tile(self) -> tuple:
        """ Get closest tile

        Returns:
            list: Tile
        """

        self.sort_tiles()

        if len(self._tiles) == 0:
            return []

        return self._tiles[0]

    def pop_closest_tile(self) -> list:
        """ Get closest tile and remove it from the list

        Returns:
            list: Tile
        """

        self.sort_tiles()
        val = self._tiles.pop(0)
        return val

    def remove_tile(self, tile: list) -> None:
        """ Remove tile from the list

        Args:
            tile (list): Tile to remove
        """

        if tile in self._tiles:
            self._tiles.remove(tile)

    @staticmethod
    def _distance(source: list, target: list) -> int:
        """ Calculate distance between two points

        Args:
            source (list): Source point [x, y]
            target (list): Target point [x, y]

        Returns:
            int: Distance
        """

        point_x, point_y = target
        player_x, player_y = source
        return sqrt((player_x - point_x)**2 + (player_y - point_y)**2)
