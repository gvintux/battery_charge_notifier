import time
import subprocess as sp
from gi.repository import Notify
from sched import scheduler


class BatteryChargeNotifier:
    AC_SHOULD_IN = 0
    AC_SHOULD_OUT = 1
    BAT_FIELD_STATE = "state"
    BAT_FIELD_PERCENTAGE = "percentage"
    BAT_STATE_CHARGING = "charging"
    BAT_STATE_DISCHARGING = "discharging"

    def __init__(self, lower_threshold, upper_threshold, interval, strings):
        self.__notification_types = ("dialog-information", "dialog-warn", "dialog-error")
        self.__style = self.__notification_types[0]
        self.__body = Notify.get_app_name()
        self.__summary = Notify.get_app_name()
        self.__notification = Notify.Notification.new(self.__body, self.__summary, self.__style)
        self.__lower_threshold = lower_threshold
        self.__upper_threshold = upper_threshold
        self.__interval = interval
        self.__strings = strings
        self.__battery = None
        self.__notified = True
        self.__scheduler = scheduler(time.time, time.sleep)
        self.find_battey()

    def find_battey(self):
        args = ("upower", "-e")
        data = None
        with sp.Popen(args, stdout=sp.PIPE) as process:
            code = process.wait()
            data = str(process.communicate()[0])
        power_sources = data.split("\\n")
        for ps in power_sources:
            if "BAT" in ps:
                self.__battery = ps
                break

    def update(self, state):
        if state == self.AC_SHOULD_IN:
            self.__body = self.__strings[0]
            self.__summary = self.__strings[1]
            self.__style = self.__notification_types[0]
        else:
            self.__body = self.__strings[2]
            self.__summary = self.__strings[3]
            self.__style = self.__notification_types[2]
        self.__notification.update(self.__body, self.__summary, self.__style)
        self.__notified = False

    def poll(self):
        args = ("upower", "-i", self.__battery)
        with sp.Popen(args, stdout=sp.PIPE) as process:
            code = process.wait()
            data = str(process.communicate()[0])
        battery_properties = data.split("\\n")
        percentage = None
        state = None
        for prop in battery_properties:
            if BatteryChargeNotifier.BAT_FIELD_PERCENTAGE in prop:
                percentage = int((prop.split(":")[1]).strip(" %"))
                break
        for prop in battery_properties:
            if BatteryChargeNotifier.BAT_FIELD_STATE in prop:
                state = str(prop.split(":")[1]).strip()
                break
        if state == BatteryChargeNotifier.BAT_STATE_DISCHARGING and percentage <= self.__lower_threshold:
            self.update(BatteryChargeNotifier.AC_SHOULD_IN)
        if state == BatteryChargeNotifier.BAT_STATE_CHARGING and percentage >= self.__upper_threshold:
            self.update(BatteryChargeNotifier.AC_SHOULD_OUT)
        if not self.__notified:
            self.notify()
            self.__notified = True

    def notify(self):
        self.__notification.show()

    def run(self):
        while True:
            self.__scheduler.enter(self.__interval, 0, self.poll)
            self.__scheduler.run()
