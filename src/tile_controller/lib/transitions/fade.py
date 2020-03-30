from lib.tile_collection import TileCollection
import time
import random


class FadeTransition:
    def __init__(self, tile_collection: TileCollection, from_effect, to_effect, delay=.5, step_size=.01, random_transition_tile_start=True, tile_delay=1):
        self.tile_collection = tile_collection
        self.from_effect = from_effect
        self.to_effect = to_effect
        self.delay = delay
        self.step_size = step_size
        self.random_transition_tile_start = random_transition_tile_start
        self.fade_transitions = {}
        self.transition_not_started = []
        self.last_updated = -1
        self.tile_delay = tile_delay
        for output_tile, from_tile, to_tile in zip(self.tile_collection.tiles, self.from_effect.tile_collection.tiles,
                                                   self.to_effect.tile_collection.tiles):
            transition = FadeTileTransition(
                output_tile, from_tile, to_tile, delay, step_size)
            self.fade_transitions[transition] = not random_transition_tile_start

            if random_transition_tile_start:
                self.transition_not_started.append(transition)

    def update(self):
        self.from_effect.update()
        self.to_effect.update()

        finished = True
        for transition, transition_started in self.fade_transitions.items():
            if not transition.update(transition_started=transition_started):
                finished = False

        if (self.last_updated == -1 or time.time() - self.last_updated >= self.tile_delay) and len(self.transition_not_started) != 0:
            index = random.randint(0, len(self.transition_not_started)-1)
            self.fade_transitions[self.transition_not_started[index]] = True
            del self.transition_not_started[index]
            self.last_updated = time.time()

        return finished


class FadeTileTransition:
    def __init__(self, output_tile, from_tile, to_tile, delay=2, step_size=0.1):
        self.output_tile = output_tile
        self.from_tile = from_tile
        self.to_tile = to_tile
        self.delay = delay
        self.last_updated = -1
        self.current_percentage = 0
        self.step_size = step_size

    def update(self, transition_started=True):
        if not transition_started:
            self.output_tile.update_color(self.from_tile.color)

        elif (self.last_updated == -1 or time.time() - self.last_updated >= self.step_size*self.delay):

            new_color = [int(self.from_tile.color[i] * (1-self.current_percentage) +
                             self.to_tile.color[i] * self.current_percentage) for i in range(3)]

            self.output_tile.update_color(new_color)

            self.current_percentage += self.step_size

            if self.current_percentage >= 1:
                self.current_percentage = 1

            self.last_updated = time.time()

        if self.current_percentage >= 1:
            return True
        else:
            return False
