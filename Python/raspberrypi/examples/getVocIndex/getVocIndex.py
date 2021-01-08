""" file getVocIndex.py
  # brief Getting VOC index
  # Copyright   [DFRobot](http://www.dfrobot.com), 2010
  # License   The MIT License (MIT)
  # author [yangfeng]<fary_young@outlook.com>
  # version  V1.0
  # date  2020-01-08
"""
import sys
sys.path.append('../../')
import time
from DFRobot_SGP40 import DFRobot_SGP40
#set IICbus elativeHumidity  temperature
mySgp40=DFRobot_SGP40(1,50,25)
#set Warm-up time
mySgp40.begin(10);
#If you want to modify the environment parameters, you can do so
#mySgp40.setEnvParams(50,-2)
while True:
    print(mySgp40.getVocIndex())
    time.sleep(1)