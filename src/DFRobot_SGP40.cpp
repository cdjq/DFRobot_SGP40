/**
*@file DFRobot_SGP40.cpp
*@brief 定义DFRobot_SGP40类的基础结构，基础方法的实现
*@copyright Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
*@SKU SEN0392
*@licence The MIT License (MIT)
*@author [wangyanfang] <yanfang.wang@dfrobot.com>
*@version V1.0
*@date 2020-12-1
*@url 
*/

#include <DFRobot_SGP40.h>

//DFRobot_SGP40::DFRobot_SGP40(){}

 /**
  * @brief  初始化函数
  * @note   检查
  * @return 返回0，初始化成功；返回其他值，初始化失败
  */
int16_t DFRobot_SGP40::begin(void)
{
  sensirion_init_sensors();//初始化SGP40,SHT,VOC算法，返回0初始化成功，其他值初始化失败
}

// /**
//  * @brief  获得序列号函数
//  * @return 返回序列号
//  */
//int16_t DFRobot_SGP40::getSerial(void)
//{
//  int16_t sgp40_probe(void);
//}

 /**
  * @brief  设置环境温湿度
  * @note   用户输入环境相对湿度和温度后，函数将他们转换成voc芯片需要的格式，之后的voc测量将依据此数据进行湿度补偿
  * @param  humidity 当前环境相对湿度值，范围0-100，单位：%RH
  * @param  temperature 当前环境温度值，范围-10~50，单位：°C
  * @return 返回0表示设置成功，返回其他值表示设置失败
  */
uint32_t DFRobot_SGP40::setRhT(float relativeHumidityRH, float temperatureC)
{
  relativeHumidity=relativeHumidityRH;
  temperature=temperatureC;
  return 0;
}

 /**
  * @brief  测量湿度补偿后的原始VOC值
  * @return 测量到的原始VOC值，范围为0-65535,单位为ticks
  */
uint16_t DFRobot_SGP40::getRawVoc(void)
{
  uint16_t sraw;
  //setRhT(relativeHumidity,temperature);
  int32_t tempC = temperature*1000;
  int32_t rh = relativeHumidity*1000;
  sgp40_measure_raw_with_rht_blocking_read(rh,tempC,&sraw);
  return sraw;
}

// /**
//  * @brief  测量湿度补偿后的原始VOC值以及周围的相对湿度和温度值
//  * @return 测量到的原始VOC值，范围为范围为0-65535,单位为ticks
//  */
//uint16_t DFRobot_SGP40::getRawVocAndRhT(void)
//{
//  
//}


 /**
  * @brief  测量湿度补偿后的VOC指数
  * @return 测量到的VOC指数，范围为0-500
  */
uint16_t DFRobot_SGP40::getVocIndex(void)
{
  int32_t voc_index;
  int32_t tempC = temperature*1000;
  int32_t rh = relativeHumidity*1000;
  //DFRobot_SGP40::setRhT(float relativeHumidityRH, float temperatureC);
  sensirion_measure_voc_index_with_rh_t(&voc_index,&rh,&tempC);
  return voc_index;
}

// /**
//  * @brief  测量湿度补偿后的VOC指数以及周围的相对湿度和温度值
//  * @param  relativeHumidity  环境相对湿度值，相对湿度单位%RH
//  * @param  temperature  环境温度值，温度单位°C
//  * @return 测量到的VOC指数，范围为0-500
//  */
//uint16_t DFRobot_SGP40::vocIndexRhT(uint8_t relativeHumidityRH=50,uint8_t temperatureC=25)
//{
//  sensirion_measure_voc_index_with_rh_t(&voc_index,&relativeHumidity,&temperature);
//}




