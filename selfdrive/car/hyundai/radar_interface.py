#!/usr/bin/env python
from cereal import car
import time


class RadarInterface(object):
  def __init__(self, CP):
    # radar
    self.pts = {}
    self.delay = 0.1

  def update(self):

<<<<<<< HEAD
    ret = car.RadarState.new_message()
=======
    ret = car.RadarData.new_message()
>>>>>>> 7d5332833b11570db288f35657a963ed0d8cad0a
    time.sleep(0.05)  # radard runs on RI updates

    return ret

if __name__ == "__main__":
  RI = RadarInterface(None)
  while 1:
    ret = RI.update()
    print(chr(27) + "[2J")
    print(ret)
