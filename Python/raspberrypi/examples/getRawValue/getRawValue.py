""" file getRawValue.py
  # brief get VOC index
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
#set IICbus  elativeHumidity  temperature
mySgp40=DFRobot_SGP40(1,50,25)
#If you want to modify the environment parameters, you can do so
#mySgp40.setEnvParams(50,-2)
while True:
    # get raw vlaue
    print 'Raw vlaue : %s'%(mySgp40.measureRaw())
    time.sleep(1)