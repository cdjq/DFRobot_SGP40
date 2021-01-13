""" 
  @file SGP40_demo_get_voc_index.py
  @brief Getting VOC index
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

#set IICbus elativeHumidity(0-100%RH)  temperature(-10~50 centigrade)
my_sgp40=DFRobot_SGP40(1,50,25)

#set Warm-up time
print 'Please wait 10 seconds...'
my_sgp40.begin(10);

#If you want to modify the environment parameters, you can do so
#elativeHumidity(0-100%RH)  temperature(-10~50 centigrade)
#mySgp40.set_envparams(50,-2)

while True:
    print 'Voc index : %d'%(my_sgp40.get_voc_index())
    time.sleep(1)