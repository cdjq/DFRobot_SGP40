/*!
 * @file getVocIndex.ino
 * @brief Read the environmental VOC index.  Range: 0-500;
 * @n Experimental phenomena: read environmental VOC index once per second and print to serial port
 *
 * @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @licence     The MIT License (MIT)
 * @author [yangfeng]<fary_young@outlook.com>
 * @version  V1.0
 * @date  2020-12-18
 * @url  
 */
#include <DFRobot_SGP40.h>
#include <Wire.h>
DFRobot_SGP40    mySgp40(&Wire);
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  mySgp40.begin();//To get the VOC index right, it will block for 10 seconds.
  mySgp40.setRhT(50,20);//relativeHumidity ：50%RH,temperature:20℃
  mySgp40.softReset();//soft reset
  mySgp40.spg40MeasureTest();//self-test
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(mySgp40.getVoclndex());
  delay(1000);
  
}
