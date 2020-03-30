class BaseTile:
    def __init__(self, pos_x, pos_y, color=(0, 0, 0)):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.calc_white = True
        self.white = None

    def update_color(self, color, calc_white=True, white=None):
        self.color = color
        self.calc_white = calc_white
        self.white = white


class Tile(BaseTile):
    def __init__(self, pos_x, pos_y, light_object, color=(0, 0, 0)):
        super().__init__(pos_x, pos_y, color)
        self.light_object = light_object

    def update_color(self, color, calc_white=True, white=None):
        super().update_color(color, calc_white=calc_white, white=white)
        self.light_object.update_color(
            color, calc_white=calc_white, white=white)

    def create_virtual_tile(self):
        return VirtualTile(self.pos_x, self.pos_y, self, self.color)


class VirtualTile(BaseTile):
    def __init__(self, pos_x, pos_y, real_tile, color=(0, 0, 0)):
        super().__init__(pos_x, pos_y, color)
        self.real_tile = real_tile

    def apply_to_real_tile(self):
        self.real_tile.update_color(
            self.color, calc_white=self.calc_white, white=self.white)
