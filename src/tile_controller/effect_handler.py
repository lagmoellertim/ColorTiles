from lib.effects.tile_or_collection.fade import Fade
from lib.effects.collection.snake import Snake
from lib.effects.collection.swap import Swap
from lib.effects.collection.highlight import Highlight
from lib.effects.tile_or_collection.color import Color
from lib.effects.tile_or_collection.strobe import Strobe
from lib.effects.collection.snake import Snake
from lib.effects.collection.slide import Slide
from lib.effects.collection.explode import Explode

from lib.transitions.fade import FadeTransition

from lib.tools import log
import time
import json


class EffectHandler:
    def __init__(self, neopixel, tile_collection):
        """Initializes the Effect Handler and sets the current effect to a static black (off)

        Arguments:
            neopixel {[Neopixel]} -- [The base neopixel object of the LED strip]
            tile_collection {[TileCollection]} -- [A Tile Collection Object]
        """

        self.neopixel = neopixel
        self.tile_collection = tile_collection
        virtual_tile_collection = self.tile_collection.create_virtual_tile_collection()
        self.current_effect = Color(virtual_tile_collection, (0, 0, 0))
        self.next_effects = []
        self.transition_running = False

        log.info("EFFECT_HANDLER", "Initialized")

    def handle_led_options(self, led_options):
        """Controls the the current effect, brightness and LED count.
        Mainly used as serial input callback to control the strip.

        Arguments:
            led_options {[dict/str]} -- [JSON string or dict of the options to apply]
        """

        if isinstance(led_options, str):
            led_options = json.loads(led_options)

        action = led_options["action"]
        data = led_options["data"]

        log.debug("EFFECT_HANDLER", "LED-Options: {}".format(led_options))

        if action == "led_options":
            if "brightness" in data.keys():
                log.info("EFFECT_HANDLER", "Change brightness")
                self.set_brightness(data["brightness"])

            if "active_led_count" in data.keys():
                log.info("EFFECT_HANDLER", "Set active led count")
                self.set_active_led_count(data["active_led_count"])

        elif action == "current_effect":
            log.info("EFFECT_HANDLER", "Set new effect")
            self.set_effect(data["effect_name"], data["options"])

        else:
            log.warning("EFFECT_HANDLER", "Unknown LED option")

    def set_brightness(self, brightness):
        """Set the brightness of the strip

        Arguments:
            brightness {[int]} -- [Brightness level (0 - 255)]
        """

        self.neopixel.brightness(brightness)

    def set_active_led_count(self, num):
        """Number of currently active LED's per corner (the inactive ones are turned off)

        Arguments:
            num {[int]} -- [Number of active LED's per corner]
        """

        for tile in self.tile_collection.tiles:
            tile.light_object.active_led_count_per_corner = num
        self.neopixel.clear()

    def set_effect(self, effect_name, options):
        """Sets the current effect with the given options, while doing a transition between the current effect and this new one

        Arguments:
            effect_name {[str]} -- [Name of the effect]
            options {[dict]} -- [Options to configure the effect]
        """

        virtual_tile_collection = self.tile_collection.create_virtual_tile_collection()

        if effect_name == "strobe":
            effect = Strobe(virtual_tile_collection, **options)
        elif effect_name == "fade":
            effect = Fade(virtual_tile_collection, **options)
        elif effect_name == "color":
            effect = Color(virtual_tile_collection, **options)
        elif effect_name == "highlight":
            effect = Highlight(virtual_tile_collection, **options)
        elif effect_name == "swap":
            effect = Swap(virtual_tile_collection, **options)
        elif effect_name == "explode":
            effect = Explode(virtual_tile_collection, **options)
        elif effect_name == "slide":
            effect = Slide(virtual_tile_collection, **options)

        self.next_effects.append(effect)
        log.info("EFFECT_HANDLER", "Added new effect")

        self.do_transition("fade")

    def do_transition(self, transition_name, options={}):
        """Creates a transition between the currently running effect and the next effect

        Arguments:
            transition_name {[str]} -- [Name of the transition (currently only fade)]

        Keyword Arguments:
            options {dict} -- [Options to configure the transition] (default: {{}})
        """

        virtual_tile_collection = self.tile_collection.create_virtual_tile_collection()

        if transition_name == "fade":
            self.current_effect = FadeTransition(
                virtual_tile_collection,
                self.current_effect,
                self.next_effects[0],
                **options
            )

            self.transition_running = True
            log.info("EFFECT_HANDLER", "Transition started")

    def run(self, refresh_rate_microseconds):
        """Mainloop to update the effects and LEDs

        Arguments:
            refresh_rate_microseconds {[float]} -- [Delay in the Mainloop to limit the refresh rate]
        """

        log.info("EFFECT_HANDLER", "Loop started")

        while True:
            try:
                if self.current_effect != None:
                    isFinished = self.current_effect.update()
                    self.current_effect.tile_collection.apply_to_real_tile_collection()

                    if self.transition_running and isFinished:
                        self.current_effect = self.next_effects.pop(0)
                        self.transition_running = False

                self.neopixel.show()
                time.sleep_ms(refresh_rate_microseconds)

            except Exception as e:
                log.exception("EFFECT_HANDLER", e)
