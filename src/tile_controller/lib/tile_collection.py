from lib.tile import Tile, VirtualTile, BaseTile


class BaseTileCollection:
    def __init__(self, tiles):
        self.tiles = tiles

    def update_color(self, color, calc_white=True, white=None):
        for tile in self.tiles:
            tile.update_color(color, calc_white=calc_white, white=white)


class TileCollection(BaseTileCollection):
    def __init__(self, tiles):
        super().__init__(tiles)

    def create_virtual_tile_collection(self):
        virtual_tiles = []

        for tile in self.tiles:
            virtual_tiles.append(tile.create_virtual_tile())

        return VirtualTileCollection(virtual_tiles)


class VirtualTileCollection(BaseTileCollection):
    def __init__(self, tiles):
        super().__init__(tiles)

    def apply_to_real_tile_collection(self):
        for tile in self.tiles:
            tile.apply_to_real_tile()
