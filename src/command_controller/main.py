import lib.wifi as wifi
from lib.mqtt import MQTT
from lib.serial import Serial
import time
from lib import log
import credentials

log.log_level = 2


wifi.activate(credentials.wifi["ap_name"], credentials.wifi["password"])

mqtt = MQTT(credentials.mqtt["host"], credentials.mqtt["username"], credentials.mqtt["password"],
            "colortiles/{}/".format(credentials.mqtt["unique_id"]), credentials.mqtt["unique_id"])

serial = Serial()

mqtt.register_callback(serial.mqtt_callback)
