from math import floor
from lib.tools.gamma import correct_gamma


class LightObject:
    def __init__(self, neopixel, start_led, led_count_per_corner, corner_count=3, active_led_count_per_corner=-1):
        self.neopixel = neopixel
        self.start_led = start_led
        self.led_count_per_corner = led_count_per_corner
        self.corner_count = corner_count

        if active_led_count_per_corner == -1:
            self.active_led_count_per_corner = self.led_count_per_corner

        else:
            self.active_led_count_per_corner = active_led_count_per_corner

    def update_color(self, color, calc_white=True, white=None):
        if white != None:
            calc_white = False

        color, calculated_white = self.__convert_color(
            color, rgbw_calc=calc_white, gamma=0)

        if self.led_count_per_corner == self.active_led_count_per_corner:
            self.neopixel.set(
                self.start_led,
                color,
                white=white if white != None else calculated_white,
                num=self.led_count_per_corner*self.corner_count,
                update=False
            )

        else:
            for corner_num in range(self.corner_count):
                self.neopixel.set(
                    self.start_led + corner_num*self.led_count_per_corner +
                    round(
                        ((self.led_count_per_corner - self.active_led_count_per_corner)/2)+.49),
                    color,
                    white=white if white != None else calculated_white,
                    num=self.active_led_count_per_corner,
                    update=False
                )

    def __convert_color(self, color, rgbw_calc=True, gamma=0):
        r = color[0]
        g = color[1]
        b = color[2]
        w = 0
        if rgbw_calc:
            w = min(color)
            r -= w
            g -= w
            b -= w

        if gamma != 0:
            r, g, b = correct_gamma(r, g, b, gamma)

        return (r << 16) + (g << 8) + b, w
