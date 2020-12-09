# DFRobot_SGP40
SGP40 是数字I2C接口的传感器。<br>
SGP40 能测量空气中的voc总量，输出的voc指数值可以指示空气质量好坏。
      输出的voc指数值范围为0-500，100为典型空气质量值，数值越大空气越差。详细的数值意义请看下面的图片。<br>
SGP40 自带VOC算法；启动时间快（小于60秒）；低功耗，散热低；十年的超长使用寿命；无需外部校准。<br>

![voc指数与空气质量对照表](https://github.com/cdjq/DFRobot_SGP40/raw/master/resources/images/vocIndex_airQuality.png)

## 产品链接（https://www.dfrobot.com/）
    SKU：SEN0392

## DFRobot_SGP40 Library for Arduino
---------------------------------------------------------
Provide an Arduino library for the SGP40 modules.

## Table of Contents

* [Summary](#summary)
* [Feature](#feature)
* [Installation](#installation)
* [Methods](#methods)
* [Compatibility](#compatibility)
* [History](#history)
* [Credits](#credits)
<snippet>
<content>

## Summary
VOC指数可通过SGP40的I2C接口读出。这些数据将通过串口打印出来。

## Feature
1. 自带voc算法，可直接输出voc指数
2. 无需外部校准
3. 超低功耗(2.6mA)，散热低
4. 启动时间<60秒
5. 十年的超长使用寿命

## Installation

To use this library, first download the library file, paste it into the \Arduino\libraries directory, then open the examples folder and run the demo in the folder.

## Methods

```C++

#include "DFRobot_SGP40.h"

 /**
  * @brief  初始化函数
  * @return 返回0表示初始化成功，返回其他值表示初始化失败
  */
  int16_t begin(void);


 /**
  * @brief  设置温湿度函数
  * @param  relativeHumidityRH  当前环境相对湿度值，范围0-100，单位：%RH
  * @param  temperatureC  当前环境温度值，范围-10~50，单位：°C
  * @return 返回0表示设置成功，返回其他值表示设置失败
  */
  uint32_t setRhT(float relativeHumidityRH=50, float temperatureC=25);

 /**
  * @brief  测量湿度补偿后的原始VOC值
  * @return 测量到的原始VOC值，范围为0-65535，单位为：ticks
  */
  uint16_t getRawVoc(void);

  /**
   * @brief  测量湿度补偿后的VOC指数
   * @return 测量到的VOC指数，范围为0-500
   */
  uint16_t getVocIndex(void);

```


## Compatibility

MCU                | Work Well | Work Wrong | Untested  | Remarks
------------------ | :----------: | :----------: | :---------: | -----
Arduino uno |       √      |             |            | 
RaspberryPi |       √      |             |            | 


## History

- data 2020-12-9
- version V0.1


## Credits

·Written by wangyanfang [yanfang.wang@dfrobot.com],2020,(Welcome to our [website](https://www.dfrobot.com/))
