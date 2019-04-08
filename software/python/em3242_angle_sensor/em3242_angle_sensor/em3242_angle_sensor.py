from __future__ import print_function
import sys
import time
import serial
import threading
import signal
import atexit


class EM3242_AngleSensor(serial.Serial):

    RESET_SLEEP_DT = 0.5
    BAUDRATE = 115200

    def __init__(self,port='/dev/ttyACM0',timeout=10.0):
        param = {'baudrate': self.BAUDRATE, 'timeout': timeout}
        super(EM3242_AngleSensor,self).__init__(port,**param)
        time.sleep(self.RESET_SLEEP_DT)

        self.lock = threading.Lock()
        self.thread = None
        self.running = False
        self._angle = 0.0

        signal.signal(signal.SIGINT,self.sigint_handler)

    @property
    def angle(self):
        with self.lock:
            angle = self._angle
        return angle


    def sigint_handler(self,signum,frame):
        self.stop()

    def start(self,callback=None):
        with self.lock:
            if self.running:
                raise EM3242_AngleSensorException, "sensor is already running"
            self.running = True
            self.callback = callback
            self.thread = threading.Thread(target=self._acquire_data)
            self.thread.daemon = True
            self.thread.start()
            self.write('b\n')

    def stop(self):
        with self.lock:
            self.write('e\n')
            self.running = False
        if self.thread is not None:
            self.thread.join()
            self.thread = None

    def _acquire_data(self):
        done = False
        while not done:
            line = ''
            with self.lock:
                while self.in_waiting > 0:
                    line = self.readline()
                    have_data = True
                done = not self.running
            if line:
                line = line.strip()
                try:
                    self._angle = float(line)
                except TypeError, ValueError:
                    continue
                if self.callback is not None:
                    self.callback(self._angle)


class EM3242_AngleSensorException(Exception):
    pass


# Testing
# ---------------------------------------------------------------------------------------
if __name__ == '__main__':

    def test_callback(angle):
        print('{:1.2f}'.format(angle))
        sys.stdout.flush()

    dev  = EM3242_AngleSensor()
    dev.start(callback=test_callback)

    while dev.running:
        time.sleep(0.1)








