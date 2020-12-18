/**
*@file DFRobot_SGP40.h
*@brief Defines the infrastructure for the DFRobot_SGP40 class
*@n This is a DFRobot_SGP40 sensor that supports IIC communication. The IIC address is immutable. The functions are as follows:
*@n Function 1: Set ambient temperature and humidity for accurate calibration. Relative humidity unit: %RH, range: 0-100; Temperature unit: °C, range: -10~50
*@n Function 2: Read VOC index , range 0-500
*@copyright Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
*@SKU SEN0392
*@licence The MIT License (MIT)
*@author [yangfeng]<fary_young@outlook.com>
*@version V1.0
*@date 2020-12-18
*@url  https://github.com/cdjq/DFRobot_SGP40
*/
#ifndef _DFROBOT_SGP40_H_
#define _DFROBOT_SGP40_H_
#include <Arduino.h>
#include <Wire.h>
extern "C" {
#include "sensirion_arch_config.h"
#include "sensirion_voc_algorithm.h"
};
#define DFRobot_SGP40_ICC_ADDR   0x59
class DFRobot_SGP40{
public:
  DFRobot_SGP40(TwoWire *pWire=&Wire);
  ~DFRobot_SGP40(){
  };
  /**
   * @brief  Initialization function
   * @return A return of 0 indicates successful initialization and a return of any other value indicates unsuccessful initialization.
   */
  uint16_t begin(void);
  /**
   * @brief  Set the temperature and humidity function
   * @param  relativeHumidityRH  Current environmental relative humidity value, range 0-100, unit: %RH
   * @param  temperatureC  Current ambient temperature, range -10~50, unit: °C
   * @return A return of 0 indicates a successful setting and any other value indicates a failed setting
   */
  uint32_t setRhT(float relativeHumidity = 50,float temperatureC=25);
  /**
   * @brief  Measure VOC index after humidity compensation
   * @return The VOC index measured ,ranged from 0 to 500
   */
  int32_t getVoclndex(void);
  /**
   * @brief  Sensor self-test
   * @return 0:all tests passed successfully; 1：one or more tests have failed
   */
  uint16_t spg40MeasureTest(void);
  /**
   * @brief  Soft Reset
   */
  void softReset(void);
private:
  /**
   * @brief  Get data through IIC
   * @return The raw data obtained
   */
  uint16_t getIICValue(void);
  /**
   * @brief  CRC
   * @param  data1  High 8 bits data
   * @param  data2  LOW 8 bits data
   * @return Calibration value
   */
  uint8_t calcCrc(uint8_t data1,uint8_t data2);
  /**
   * @brief  Conversion of relative humidity in % and temperature in °C into ticks as the input parameters of the measurement command
   */
  void dataTransformation(void);
  /**
   * @brief  spg40 Heater Off
   */
  void spg40HeaterOff(void);
  /**
   * @brief  Write commands through IIC
   * @param  Command  Command address
   * @param  len  Command len
   */
  void IICWrite(uint8_t* Command,uint8_t len);
private:
  TwoWire* _pWire;
  float _relativeHumidity;
  float _temperatureC;
  uint8_t _rhTemData[8];
  uint8_t _deviceAddr;
  VocAlgorithmParams _vocaAgorithmParams;
};
#endif
