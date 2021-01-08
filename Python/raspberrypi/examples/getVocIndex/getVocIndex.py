import sys
sys.path.append('../')
import time
from DFRobot_SGP40 import DFRobot_SGP40
#set IICbus、relativeHumidity and temperature
mySgp40=DFRobot_SGP40(1,50,25)
#set Warm-up time
mySgp40.begin(10);
#If you want to modify the environment parameters, you can do so
#mySgp40.setEnvParams(50,-2)
while True:
    print(mySgp40.getVocIndex())
    time.sleep(1)