from __future__ import print_function
import sys
import time
from em3242_angle_sensor import EM3242_AngleSensor

def test_callback(angle):
    print('{:1.2f}'.format(angle))
    sys.stdout.flush()

dev  = EM3242_AngleSensor()
dev.start(callback=test_callback)

while dev.running:
    time.sleep(0.1)








