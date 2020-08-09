import time
from machine import Pin


class PIR(object):

    def __init__(self, pin='G5', hold_time_sec=5, last_trigger=-5):
        self.pir = Pin(pin, mode=Pin.IN, pull=Pin.PULL_UP)
        self.count_last_hour = 0
        self.hold_time_sec = hold_time_sec
        self.last_trigger = last_trigger

    def run_pir(self):
        while True:
            if self.pir() == 1:
                if time.time() - self.last_trigger > self.hold_time_sec:
                    self.last_trigger = time.time()
                    self.count_last_hour += 1
            else:
                self.last_trigger = 0

            time.sleep_ms(500)

    def get_count_last_h(self):
        tmp = self.count_last_hour
        self.count_last_hour = 0
        return tmp
