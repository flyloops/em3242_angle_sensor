from __future__ import print_function
import sys
import time
from em3242_angle_sensor import EM3242_AngleSensor


dev  = EM3242_AngleSensor()
dev.start()

while dev.running:
    print(dev.angle)
    sys.stdout.flush()
    time.sleep(0.02)








