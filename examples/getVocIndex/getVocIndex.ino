/*!
 * @file getVocIndex.ino
 * @brief Read the environmental VOC index.  Range: 0-500;
 * @n Experimental phenomena: read environmental VOC index once per second and print the value in serial port
 *
 * @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @licence     The MIT License (MIT)
 * @author [yangfeng]<fary_young@outlook.com>
 * @version  V1.0
 * @date  2020-12-18
 * @url  
 */
#include <DFRobot_SGP40.h>

/*方法一：自定义传入的I2C指针:软I2C*/
//#include <softwareWire.h>
//DFRobot_SGP40    mySgp40(&softwareWire(4,5));

/*
 * 方法二：默认传入*pWire=&Wire
 * I2C 默认地址：0x59
 */
//DFRobot_SGP40    mySgp40(&Wire);
DFRobot_SGP40    mySgp40;


void setup() {
  
  Serial.begin(115200);
  
  //To get the VOC index right, it will block for 10 seconds.
  while(mySgp40.begin() !=0){
    Serial.println("failed to init chip, please check if the chip connection is fine");
    delay(1000);
  }
  Serial.println("sgp40 initialized successfully ！");
  /* 
   * @breif 设置当前环境中的相对湿度和温度
   * @note  传感器内部已进行温湿度校准，若需要得到更精确的voc指数，请打开注释
   * @param relativeHumidity：相对湿度，指空气中的水汽含量。范围：0-100，单位：%RH，例如：50%
   * @param temperature：温度。范围：-10~50，单位：°C，例如：20°C
   */
  //mySgp40.setRhT(/*relativeHumidity = */ 50, /*temperature = */ 20);
  
}

void loop() {
  /* 
   * @breif  获取voc指数
   * @note   voc指数可直接指示空气质量的好坏。数值越大，空气质量越差
   * @note   0-100，空气质量良好
   * @note   100-200，空气质量较好，无需通风
   * @note   200-400，空气质量较差，需要通风
   * @note   400-500，空气质量极差，需强烈通风
   * @return 返回voc指数，范围：0-500
   */
  uint16_t index = mySgp40.getVoclndex();
  
  Serial.print("vocIndex = ");
  Serial.println(index);
  delay(1000);
}
