from lib.tile_collection import TileCollection


class Color:
    def __init__(self, tile_collection: TileCollection, color=(0, 0, 0)):
        self.tile_collection = tile_collection
        self.color = color

    def update(self):
        self.tile_collection.update_color(self.color)
