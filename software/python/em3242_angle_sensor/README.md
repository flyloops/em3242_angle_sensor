em3242_angle_sensor
--------
A Python library which provides a simple serial interface to the EM3242 angle sensor. 

Example
--------

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


Installation
------------

```
#!bash

$ python setup.py install 


```


Links
-----

* Download https://github.com/willdickson/em3242_angle_sensor
* Documentation [TODO] 


