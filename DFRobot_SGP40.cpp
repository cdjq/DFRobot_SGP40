/**
*@file DFRobot_SGP40.cpp
*@brief Define the DFRobot_SGP40 class infrastructure, the implementation of the underlying methods
*@copyright Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
*@SKU SEN0392
*@licence The MIT License (MIT)
*@author [yangfeng]<fary_young@outlook.com>
*@version V1.0
*@date 2020-12-18
*@url https://github.com/cdjq/DFRobot_SGP40
*/
#include <DFRobot_SGP40.h>
#include "sensirion_arch_config.h"
#include "sensirion_voc_algorithm.h"
DFRobot_SGP40::DFRobot_SGP40(TwoWire *pWire)
{
  _pWire = pWire;
  _deviceAddr = DFRobot_SGP40_ICC_ADDR;
  _relativeHumidity = 50;
  _temperatureC = 25;
}
uint16_t DFRobot_SGP40::begin(void)
{
  _pWire->begin();
  VocAlgorithm_init(&_vocaAgorithmParams);
  int time = millis();
  while(millis()-time<10000){
    getVoclndex();
  }
  return spg40MeasureTest();
}
uint8_t DFRobot_SGP40::calcCrc(uint8_t data1,uint8_t data2)
{
  uint8_t crc = 0xFF;
  uint8_t data[2];
  data[0]=data1;
  data[1]=data2;
  for(int i =0; i<2;i++){
    crc ^= data[i];
    for(uint8_t bit = 8;bit>0;--bit){
      if(crc & 0x80){
        crc = (crc << 1)^0x31u;
      }else{
        crc = (crc << 1);
      }
    }
  }
  return crc;
}
uint32_t DFRobot_SGP40::setRhT(float relativeHumidity, float temperatureC)
{
  _relativeHumidity = relativeHumidity;
  _temperatureC = temperatureC;
  dataTransformation();
  IICWrite(_rhTemData,6);
  return 0;
}
void DFRobot_SGP40::dataTransformation(void)
{
  uint16_t RH = (uint16_t)((_relativeHumidity*65535)/100+0.5);
  uint16_t TemC = (uint16_t)((_temperatureC+45)*(65535/175)+0.5);
  _rhTemData[0]=0x26;
  _rhTemData[1]=0x0F;
  _rhTemData[2]=RH>>8;
  _rhTemData[3]=RH&0x00FF;
  _rhTemData[4]=calcCrc(_rhTemData[2],_rhTemData[3]);
  _rhTemData[5]=TemC>>8;
  _rhTemData[6]=TemC&0x00FF;
  _rhTemData[7]=calcCrc(_rhTemData[5],_rhTemData[6]);
}
void DFRobot_SGP40::IICWrite(uint8_t* Command,uint8_t len)
{
  _pWire->beginTransmission(_deviceAddr);
  for(uint8_t i=0;i<len;i++){
    _pWire->write(Command[i]);
  }
  _pWire->endTransmission();
}
uint16_t DFRobot_SGP40::getIICValue()
{
  uint8_t data[3]={0,0,0};
  uint16_t value=0;
  _pWire->requestFrom(_deviceAddr,3);
  for(uint8_t i=0;i<3;i++){
    data[i]=_pWire->read();
  }
  value=(data[0]<<8)|data[1];
  return value;
}
int32_t DFRobot_SGP40::getVoclndex(void)
{
  uint8_t data[3]={0,0,0};
  int32_t value;
  int32_t vocIndex=0;
  dataTransformation();
  _pWire->beginTransmission(_deviceAddr);
  for(int i=0;i<8;i++){
    _pWire->write(_rhTemData[i]);
  }
  _pWire->endTransmission();
  delay(30);
  _pWire->requestFrom(_deviceAddr,3);
  for(uint8_t i=0;i<3;i++){
    data[i]=_pWire->read();
  }
  value=(data[0]<<8)|data[1];
  VocAlgorithm_process(&_vocaAgorithmParams, value, &vocIndex);
  return vocIndex;
}
void DFRobot_SGP40::spg40HeaterOff()
{
  uint8_t testCommand[2]={0x36,0x15};
  IICWrite(testCommand,2);
}
uint16_t DFRobot_SGP40::spg40MeasureTest()
{
  uint8_t testCommand[2]={0x28,0x0E};
  uint16_t value=0;
  IICWrite(testCommand,2);
  delay(250);
  if(getIICValue()==0xD400){
    return 0;
  }
  return 1;
}
void DFRobot_SGP40::softReset()
{
  uint8_t testCommand[2]={0x00,0x06};
  IICWrite(testCommand,2);
}











