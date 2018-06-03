import gi
import os
import sys

gi.require_version("Notify", "0.7")
sys.path.append(os.path.realpath(os.path.curdir))
from gi.repository import Notify
from .battery_charge_notifier import BatteryChargeNotifier


def load_config():
    file = open(
        os.path.realpath(os.curdir) + os.sep + "battery_charge_notifier" + os.sep + "battery_charge_notifier.conf")
    interval = None
    lower_threshold = None
    upper_threshold = None
    strings = [None, None, None, None]

    for line in file:
        if not line.startswith("#"):
            key, value = line.split("=", maxsplit=2)
            key = key.strip()
            value = value.strip().strip("\"")
            if "interval" == key:
                interval = value
            if "lower_threshold" == key:
                lower_threshold = value
            if "upper_threshold" == key:
                upper_threshold = value
            if "battery_low_body" == key:
                strings[0] = value
            if "battery_low_summary" == key:
                strings[1] = value
            if "battery_up_body" == key:
                strings[2] = value
            if "battery_up_summary" == key:
                strings[3] = value
    return int(interval), int(lower_threshold), int(upper_threshold), strings


Notify.init("Battery Charge Notifier")
config = load_config()
notifier = BatteryChargeNotifier(interval=config[0],
                                 lower_threshold=config[1], upper_threshold=config[2],
                                 strings=config[3])
notifier.run()
