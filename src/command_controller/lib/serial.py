import machine
import json
import time
from lib import log


class Serial:
    def __init__(self, channel=1, rx=16, tx=17, baudrate=115200, parity=1, buffer_size=4096):
        """Initialize the UART Connection with the given settings

        Keyword Arguments:
            channel {int} -- [UART-Channel] (default: {1})
            rx {int} -- [Receive-Pin] (default: {16})
            tx {int} -- [Transceive-Pin] (default: {17})
            baudrate {int} -- [Baudrate] (default: {115200})
            parity {int} -- [Parity] (default: {1})
            buffer_size {int} -- [Buffer Size] (default: {4096})
        """

        self.uart = machine.UART(
            channel, rx=rx, tx=tx, baudrate=baudrate,
            parity=parity, buffer_size=buffer_size
        )

        self.uart.init()
        log.info("Serial: UART initialized")

    def send_string(self, s, segmentSize=240):
        """Sends a string via UART. The string is divided into segments, in order too avoid memory overflow on the receiving device.

        Arguments:
            s {[str]} -- [The string to send via UART]

        Keyword Arguments:
            segmentSize {int} -- [The character count after which a new segment is created] (default: {240})
        """
        log.info("Serial: Send Data")
        log.debug("Serial: String: {} - SegmentSize: {}".format(s, segmentSize))
        for segment in tuple(s[i:i+segmentSize]+"[SEG]" for i in range(0, len(s), segmentSize)):
            log.debug("Serial: Segment: {}".format(segment))
            self.uart.write(segment)
            time.sleep_ms(20)

    def send_data(self, data, tag):
        """Send a dictionary with tag attribute via UART. Different tags can be treated differently on the receiver.

        Arguments:
            data {[dict]} -- [Dictionary of data]
            tag {[str]} -- [Tag attribute to differentiate message types on receiver]
        """
        s = "{}[{}]".format(json.dumps(data), tag)
        self.send_string(s)

    def mqtt_callback(self, data):
        """Default callback for MQTT messages. Same as send_data, but with tag set to 'MQTT'

        Arguments:
            data {[dict]} -- [MQTT data]
        """
        self.send_data(data, "MQTT")
