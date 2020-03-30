import machine
from lib.tools import log


def remove_suffix(text, suffix):
    if not text.endswith(suffix):
        return text
    return text[:len(text)-len(suffix)]


class Serial:
    def __init__(self):
        self.message_buffer = []

        self.uart = machine.UART(1, tx=17, rx=16, parity=1, buffer_size=4096)
        self.uart.init(parity=1, buffer_size=4096)
        log.info("SERIAL", "Initialized")

        self.uart.callback(self.uart.CBTYPE_PATTERN,
                           self.on_data_receive, pattern="[SEG]")

        self.callbacks = {}

    def register_callback(self, tag, callback):
        self.callbacks[tag] = callback

    def on_data_receive(self, data_container):
        data = data_container[2]

        log.info("SERIAL", "Segment received")
        log.debug("SERIAL", "Segment: {}".format(data))

        self.message_buffer.append(data)

        message_buffer_string = "".join(self.message_buffer)

        for tag, callback in self.callbacks.items():
            if message_buffer_string.endswith("[{}]".format(tag)):
                data_string = remove_suffix(
                    message_buffer_string, "[{}]".format(tag))

                log.info("SERIAL", "Complete Message received")
                log.debug(
                    "SERIAL", "Message: {} - Tag: {}".format(data_string, tag))

                self.message_buffer = []
                callback(data_string)
