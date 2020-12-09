/**
*@file DFRobot_SGP40.h
*@brief 定义DFRobot_SGP40类的基础结构
*@n 这是一个DFRobot_SGP40传感器，支持IIC通信,IIC地址不可改变,功能如下
*@n 功能1：设置环境温湿度，进行精确校准。相对湿度单位：%RH，范围：0-100；温度单位：°C，范围：-10~50
*@n 功能2：读取原始voc值，rawVoc，单位：
*@n 功能3：读取voc指数，vocIndex，范围0-500
*@copyright Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
*@SKU SEN0392
*@licence The MIT License (MIT)
*@author [wangyanfang] <yanfang.wang@dfrobot.com>
*@version V1.0
*@date 2020-12-1
*@url  
*/

#ifndef DFROBOT_SGP40_H
#define DFROBOT_SGP40_H

#if ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

#include "sgp40_voc_index/sgp40.h"
#include "sgp40_voc_index/sgp40_voc_index.h"


//#define ENABLE_DBG

#ifdef ENABLE_DBG
#define DBG(...) {Serial.print("[");Serial.print(__FUNCTION__); Serial.print("(): "); Serial.print(__LINE__); Serial.print(" ] "); Serial.println(__VA_ARGS__);}
#else
#define DBG(...)
#endif

class DFRobot_SGP40
{
public:
 /**
  * @brief  初始化函数
  * @return 返回0表示初始化成功，返回其他值表示初始化失败
  */
  int16_t begin(void);
  
// /**
//  * @brief  获得序列号函数
//  * @return 返回序列号
//  */
//  int16_t getSerial(void);
  
 /**
  * @brief  设置温湿度函数
  * @param  relativeHumidityRH  当前环境相对湿度值，范围0-100，单位：%RH
  * @param  temperatureC  当前环境温度值，范围-10~50，单位：°C
  * @return 返回0表示设置成功，返回其他值表示设置失败
  */
  uint32_t setRhT(float relativeHumidityRH=50, float temperatureC=25);
  
 /**
  * @brief  测量湿度补偿后的原始VOC值
  * @return 测量到的原始VOC值，范围为0-65535，单位为：ticks（此处想要修改使其变为ppm为单位的值）
  */
  uint16_t getRawVoc(void);
  
  
  /**
   * @brief  测量湿度补偿后的VOC指数
   * @return 测量到的VOC指数，范围为0-500
   */
  uint16_t getVocIndex(void);
  
  
  private:
    float relativeHumidity = 50;
    float temperature = 25;
  
};
#endif
