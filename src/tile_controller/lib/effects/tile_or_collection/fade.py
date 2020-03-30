from lib.tile_collection import TileCollection
from lib.tools import color as colorlib
import time


class Fade:
    def __init__(self, tile_collection: TileCollection, colors, delay=5, step_size=.01, step_offset=0, hsv=True,
                 repeat=False):

        self.tile_collection = tile_collection
        self.colors = colors
        self.color = None
        self.current_frame_index = [0, 1]
        self.current_step = 0
        self.total_steps = 0
        self.delay_per_step = 0
        self.frame_difference = None
        self.step_size = step_size
        self.delay = delay
        self.last_updated = -1
        self.step_offset = step_offset
        self.hsv = hsv
        self.repeat = repeat
        self.finished = False

    def update(self):
        if self.finished or (not self.repeat and (self.current_frame_index[1] == 0 and self.last_updated != -1)):
            self.finished = True
            return True

        if self.current_step == 0:
            self.calculate_current_frame()

        if self.last_updated == -1 and self.step_offset != 0:
            self.current_step = self.step_offset

            while self.total_steps <= self.current_step:
                self.current_step -= self.total_steps
                self.current_frame_index = [
                    (i + 1) % len(self.colors) for i in self.current_frame_index]
                self.calculate_current_frame()

            self.color = [self.color[i] + self.frame_difference[i]
                          * self.current_step for i in range(3)]

        if self.hsv:
            color = colorlib.hsv_to_rgb(*self.color)
        else:
            color = self.color

        # print(color)

        self.tile_collection.update_color([int(i) for i in color])

        if self.last_updated == -1 or time.ticks_diff(time.ticks_ms(), self.last_updated) >= self.delay_per_step*1000:
            if self.current_step >= self.total_steps:
                self.current_frame_index = [
                    (i+1) % len(self.colors) for i in self.current_frame_index]
                self.current_step = 0
                return False

            for i in range(3):
                self.color[i] += self.frame_difference[i]

                if self.hsv:
                    self.color[0] %= 1

            self.current_step += 1

            self.last_updated = time.ticks_ms()

        return False

    def calculate_current_frame(self):
        if self.hsv:
            color_1 = colorlib.rgb_to_hsv(
                *self.colors[self.current_frame_index[0]])
            color_2 = colorlib.rgb_to_hsv(
                *self.colors[self.current_frame_index[1]])
        else:
            color_1 = self.colors[self.current_frame_index[0]]
            color_2 = self.colors[self.current_frame_index[1]]

        self.frame_difference = [
            (color_2[i]-color_1[i])*(self.step_size/self.delay) for i in range(3)]

        if self.hsv and abs(color_2[0] - color_1[0]) > 1 - abs(color_2[0] - color_1[0]):
            new_hue_difference = (
                1 - color_2[0] - color_1[0])*(self.step_size/self.delay)

            if color_1[0] < color_2[0]:
                self.frame_difference[0] = -new_hue_difference
            else:
                self.frame_difference[0] = new_hue_difference

        self.total_steps = int(1 / self.step_size+.49) * self.delay
        self.delay_per_step = self.delay / self.total_steps
        self.color = list(color_1)
