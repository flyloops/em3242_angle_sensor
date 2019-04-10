## EM3242 Angle Sensor 

Firmware + Python library for collecting data from the EM3242 absolute angle sensor.

## Firmware

* Location: "firmware" sub-directory
* Platform: teensy 3.2
* Install using Aruduino IDE w/ Teensduino Addon

## Python Library

* Location: "softare/python/em3242_angle_sensor"
* Requirements: pyserial


## Example

```python

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

```

### Installation


```bash
python setup.py install
```

