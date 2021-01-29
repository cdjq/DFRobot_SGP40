  
/*!
 * @file getVocIndex.ino
 * @brief Read the environmental VOC index.  Range: 0-500;
 * @n Experimental phenomena: read environmental VOC index once per second and print the value in serial port
 *
 * @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @licence     The MIT License (MIT)
 * @author [yangfeng]<feng.yang@dfrobot.com>
 * @version  V1.0
 * @date  2020-12-18
 * @get from https://www.dfrobot.com
 * @url  https://github.com/DFRobot/DFRobot_SGP40
 */
#include <DFRobot_SGP40.h>

/* 
 * Method 1: pass in the specified I2C object address 
 * #include <Wire.h>
 * DFRobot_SGP40    mySgp40(&Wire);
 
 * Method 2: use the default I2C object&Wire
 * I2C Default Address：0x59
 */

//#include <Wire.h>
//DFRobot_SGP40    mySgp40(&Wire);
DFRobot_SGP40    mySgp40;


void setup() {
  Serial.begin(115200);
  Serial.println("sgp40 is starting, the reading can be taken after 10 seconds...");
  /*
   * Sensor preheat time: 10s
   * duration: init wait time. Unit: ms. It is suggested: duration>=10000ms
   */
  while(mySgp40.begin(/*duration = */10000) !=true){
    Serial.println("failed to init chip, please check if the chip connection is fine");
    delay(1000);
  }
  Serial.println("----------------------------------------------");
  Serial.println("sgp40 initialized successfully!");
  Serial.println("----------------------------------------------");
  /* 
   * Set the relative humidity and temperature of current environment 
   * The sensor has internal temerpature & humidity calibration. For more accurate VOC index, please open the function setRhT().
   * relativeHumidity：ambient relative humidity, refer to the moisture content in air. Range：0-100, unit: %RH，e.g. 50%
   * temperature：ambient temperature. Range: -10~50, unit: °C, e.g. 20°C
   */
  //mySgp40.setRhT(/*relativeHumidity = */ 50, /*temperature = */ 20);
  
}

void loop() {
  /* 
   * Get VOC index 
   * VOC index can directly indicates the condition of air quality. The larger the value, the worse the air quality
   *    0-100，no need to ventilate,purify
   *    100-200，no need to ventilate,purify
   *    200-400，ventilate,purify
   *    400-500，ventilate,purify intensely
   * Return VOC index, range: 0-500
   */
  uint16_t index = mySgp40.getVoclndex();
  
  Serial.print("vocIndex = ");
  Serial.println(index);
  delay(1000);
}
