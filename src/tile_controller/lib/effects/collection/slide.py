from lib.tile_collection import TileCollection
from lib.effects.tile_or_collection.fade import Fade
import time
import random


class Slide:
    def __init__(self, tile_collection: TileCollection, colors, speed=1, direction="left"):
        self.tile_collection = tile_collection
        self.colors = colors
        self.speed = speed
        self.delay = .2*speed
        self.last_updated = None
        self.last_updated_color_change = None
        self.current_zone = 0
        self.animation_map = {}
        self.distance_zones = []
        self.delay_color_change = 2*speed

        self.calculate_zones(direction)

    def calculate_zones(self, direction):
        distance_zones_map = {}
        self.distance_zones = []

        for tile in self.tile_collection.tiles:
            if direction == "bottom" or direction == "top":
                distance = tile.pos_y
            else:
                distance = tile.pos_x

            if not distance in distance_zones_map.keys():
                distance_zones_map[distance] = []

            distance_zones_map[distance].append(tile)

        for i in sorted(distance_zones_map.keys()):
            if direction == "top" or direction == "right":
                self.distance_zones.insert(0, distance_zones_map[i])
            else:
                self.distance_zones.append(distance_zones_map[i])

    def update(self):
        if self.last_updated == None:
            self.color = random.choice(self.colors)
            self.next_color = random.choice(
                [x for x in self.colors if x != self.color])
            self.tile_collection.update_color(self.color)

        if self.last_updated_color_change == None or time.ticks_diff(time.ticks_ms(), self.last_updated_color_change) >= self.delay_color_change*1000:
            for tile, animation in self.animation_map.items():
                finished = animation.update()
                if finished and tile in self.distance_zones[-1]:
                    self.animation_map = {}

                    self.color = self.next_color
                    self.next_color = random.choice(
                        [x for x in self.colors if x != self.color])

                    self.current_zone = 0

                    self.last_updated_color_change = time.ticks_ms()

                    return

            if (self.last_updated == None or time.ticks_diff(time.ticks_ms(), self.last_updated) >= self.delay*1000) and self.current_zone < len(self.distance_zones):
                for tile in self.distance_zones[self.current_zone]:
                    effect = Fade(tile, colors=[
                        self.color, self.next_color], repeat=False, delay=.3*self.speed, step_size=.01, hsv=1)
                    #print(self.color, self.next_color)
                    self.animation_map[tile] = effect

                self.current_zone += 1
                self.last_updated = time.ticks_ms()
