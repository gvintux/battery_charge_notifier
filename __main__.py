import gi
import os
import sys

gi.require_version('Notify', '0.7')
sys.path.append(os.path.realpath(os.path.curdir))
from gi.repository import Notify
from .battery_charge_notifier import *


def load_config():
    file = open(
        os.path.realpath(os.curdir) + os.sep + "battery_charge_notifier" + os.sep + "battery_charge_notifier.conf")
    interval = None
    lower_threshold = None
    upper_threshold = None
    strings = [None, None, None, None]

    for line in file:
        if not line.startswith("#"):
            if "interval" in line:
                interval = line.split("=")[1].strip()
            if "lower_threshold" in line:
                lower_threshold = line.split("=")[1].strip()
            if "upper_threshold" in line:
                upper_threshold = line.split("=")[1].strip()
            if "battery_low_body" in line:
                strings[0] = line.split("=")[1].strip()
            if "battery_low_summary" in line:
                strings[1] = line.split("=")[1].strip()
            if "battery_up_body" in line:
                strings[2] = line.split("=")[1].strip()
            if "battery_up_summary" in line:
                strings[3] = line.split("=")[1].strip()
    return int(interval), int(lower_threshold), int(upper_threshold), strings


Notify.init("Battery Charge Notifier")
config = load_config()
notifier = BatteryChargeNotifier(interval=config[0],
                                 lower_threshold=config[1], upper_threshold=config[2],
                                 strings=config[3])
notifier.run()
