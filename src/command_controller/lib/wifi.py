import network
import time
from lib import log


def activate(ap_name, password, debug=False):
    """Actives and connects to a WIFI network with a given name and password

    Arguments:
        ap_name {[str]} -- [Accesspoint-Name]
        password {[str]} -- [Accesspoint-Password]
    """

    wlan = network.WLAN()
    wlan.active(True)

    log.info("WiFi: Activated")

    time.sleep(4)

    wlan.connect(ap_name, password)
    log.info("WiFi: Trying to connect ...")
    start = time.time()

    while not wlan.isconnected() and (time.time() - start < 30):
        time.sleep_ms(200)

    if wlan.isconnected():
        log.success("WiFi: Connected")
    else:
        log.error("WiFi: Connection failed")
