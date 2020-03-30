from lib.tile_collection import TileCollection
import time


class Strobe:
    def __init__(self, tile_collection: TileCollection, colors=None, delay=.5):
        if colors is None:
            colors = [(0, 0, 0), (255, 255, 255)]
        self.tile_collection = tile_collection
        self.colors = colors
        self.delay = delay
        self.last_updated = None
        self.current_index = 0

    def update(self):
        if self.last_updated == None or time.ticks_diff(time.ticks_ms(), self.last_updated) >= self.delay:

            for tile in self.tile_collection.tiles:
                tile.update_color(self.colors[self.current_index])

            self.current_index = (self.current_index + 1) % len(self.colors)

            self.last_updated = time.ticks_ms()
