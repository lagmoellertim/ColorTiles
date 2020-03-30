from lib.tools import log
import machine
from lib.tools import color
from lib.light_object import LightObject
from lib.tile import Tile
from lib.tile_collection import TileCollection
from effect_handler import EffectHandler
import gc
from serial import Serial

log.info("MAIN", "Libraries loaded. Initializing ...")

gc.threshold(70000)
machine.freq(240000000)

led_data_power_control = machine.Pin(19, machine.Pin.OUT)
led_data_power_control.value(1)

neopixel = machine.Neopixel(machine.Pin(5), 300, machine.Neopixel.TYPE_RGBW)

color.np = neopixel
neopixel.clear()
neopixel.brightness(255)

tiles = []

xy = [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
      (4, 0), (5, 0), (6, 0), (6, 1), (1, 12)]

for i in range(len(xy)):
    tiles.append(Tile(xy[i][0], xy[i][1], LightObject(
        neopixel, 1+i*15, 5, corner_count=3, active_led_count_per_corner=5)))

tile_collection = TileCollection(tiles)
effect_handler = EffectHandler(neopixel, tile_collection)

serial = Serial()
serial.register_callback("MQTT", effect_handler.handle_led_options)

fps = 60
refresh_rate_microseconds = int((1/fps)*1000)

log.success("MAIN", "Successfully initialized")

effect_handler.run(refresh_rate_microseconds)
