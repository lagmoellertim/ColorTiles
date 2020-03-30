from lib.tile_collection import BaseTileCollection
from lib.effects.tile_or_collection.fade import Fade


class Snake:
    def __init__(self, tile_collection: BaseTileCollection, color=(0, 0, 0)):
        self.tile_collection = tile_collection
        self.color = color

        self.effects = []

        for i, tile in enumerate(tile_collection.tiles):
            self.effects.append(
                Fade(tile, step_offset=5*i, colors=[(255, 1, 0), (0, 255, 0), (0, 0, 255)], hsv=False, repeat=True, delay=1.5, step_size=0.05))

    def update(self):
        for effect in self.effects:
            effect.update()

        # for tile in self.tile_collection.tiles:
        #    if not tile.color == self.color:
        #        tile.update_color(self.color)
