from lib.tile_collection import TileCollection
from lib.effects.tile_or_collection.fade import Fade
import time
import random


class Swap:
    def __init__(self, tile_collection: TileCollection, colors, delay=.2, maximum_active_tiles=5):
        self.tile_collection = tile_collection
        self.colors = colors
        self.delay = delay
        self.last_updated = None
        self.maximum_active_tiles = maximum_active_tiles
        self.currently_available = []
        self.animation_map = {}

        for tile in self.tile_collection.tiles:
            self.currently_available.append(tile)

    def update(self):
        if self.last_updated == None:
            random_color = random.choice(self.colors)
            self.tile_collection.update_color(random_color)

        for animation, tile in self.animation_map.items():
            a = animation.update()
            if a:
                self.currently_available.append(tile)
                # del self.animation_map[animation]
                self.animation_map.pop(animation, None)

        if (self.last_updated == None or time.ticks_diff(time.ticks_ms(), self.last_updated) >= self.delay*1000) and len(self.animation_map) == 0:
            for i in range(random.randint(0, self.maximum_active_tiles)):
                tile = random.choice(self.currently_available)

                random_color = random.choice(
                    [x for x in self.colors if x != tile.color])

                effect = Fade(tile, colors=[
                              tile.color, random_color], repeat=False, delay=1.5, step_size=.01, hsv=0)

                # print(random_color)

                self.animation_map[effect] = tile
                self.currently_available.remove(tile)

            self.last_updated = time.ticks_ms()
