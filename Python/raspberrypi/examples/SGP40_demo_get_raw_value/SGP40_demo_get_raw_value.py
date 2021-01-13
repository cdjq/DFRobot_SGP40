""" 
  @file SGP40_demo_get_raw_value.py
  @brief brief get VOC index
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @licence     The MIT License (MIT)
  @author      [yangfeng]<fary_young@outlook.com> 
  version  V1.0
  date  2021-01-12
  @get from https://www.dfrobot.com
  @url https://github.com/cdjq/DFRobot_SGP40
"""
import sys
sys.path.append('../../')
import time
from DFRobot_SGP40 import DFRobot_SGP40


#set IICbus  elativeHumidity  temperature
my_sgp40=DFRobot_SGP40(1,50,25)


#If you want to modify the environment parameters, you can do so
#my_sgp40.set_envparams(50,-2)

while True:
    # get raw vlaue
    print 'Raw vlaue : %d'%(my_sgp40.measure_raw())
    time.sleep(1)