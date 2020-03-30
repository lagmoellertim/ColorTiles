import network
import json
import time
import network
from lib import log


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


class MQTT:
    def __init__(self, host, user, password, base_path, client_id, debug=False):
        self.base_path = base_path
        self.debug = debug
        self.callback = None

        self.mqtt = network.mqtt(
            "mqtt", host, user=user, password=password, autoreconnect=True,
            data_cb=self.on_message_receive, cleansession=True, clientid=client_id
        )

        self.mqtt.start()

        log.info("MQTT: Started. Trying to connect ...")

        while not self.mqtt.status()[0] == 2:
            time.sleep_ms(200)

        log.success("MQTT: Connected")
        self.mqtt.subscribe('{}+'.format(self.base_path))

    def register_callback(self, callback):
        self.callback = callback

    def on_message_receive(self, message):
        _, topic, message_str = message
        log.info("MQTT: Message received")
        log.debug("MQTT: Topic: {} - Message: {}".format(topic, message_str))

        if self.callback is not None:
            self.callback({
                "action": remove_prefix(topic, self.base_path),
                "data": json.loads(message_str)
            })
