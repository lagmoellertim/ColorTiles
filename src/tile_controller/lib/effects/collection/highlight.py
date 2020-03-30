from lib.tile_collection import TileCollection
from lib.effects.tile_or_collection.fade import Fade
import time
import random


class Highlight:
    def __init__(self, tile_collection: TileCollection, base_color, highlight_colors, delay=.2, maximum_active_tiles=5, highlight_different_colors=False):
        self.tile_collection = tile_collection
        self.base_color = base_color
        self.highlight_colors = highlight_colors
        self.delay = delay
        self.last_updated = None
        self.maximum_active_tiles = maximum_active_tiles
        self.currently_available = []
        self.animation_map = {}
        self.highlight_different_colors = highlight_different_colors

        for tile in self.tile_collection.tiles:
            self.currently_available.append(tile)

    def update(self):
        self.tile_collection.update_color(self.base_color)

        for animation, tile in self.animation_map.items():
            a = animation.update()
            if a:
                self.currently_available.append(tile)
                self.animation_map.pop(animation, None)

        if (self.last_updated == None or time.ticks_diff(time.ticks_ms(), self.last_updated) >= self.delay*1000) and len(self.animation_map) == 0:
            random_color = random.choice(self.highlight_colors)
            for i in range(random.randint(0, self.maximum_active_tiles)):
                tile = random.choice(self.currently_available)

                effect = Fade(tile, colors=[
                              self.base_color, random_color, self.base_color], repeat=False, delay=1.5, step_size=.01, hsv=0)

                # print(random_color)

                self.animation_map[effect] = tile
                self.currently_available.remove(tile)

                if self.highlight_different_colors:
                    random_color = random.choice(self.highlight_colors)

            self.last_updated = time.ticks_ms()
