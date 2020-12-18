# DFRobot_SGP40
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
VOC indices can be read through SGP40's I2C interface. The data will be printed through a serial port.

## Feature

1.  Set ambient temperature and humidity for accurate calibration. Relative humidity unit: %RH, range: 0-100; Temperature unit: °C, range: -10~50
2.  Read VOC index , range 0-500

## Installation

To use this library, first download the library file, paste it into the \Arduino\libraries directory, then open the examples folder and run the demo in the folder.

## Methods

```C++

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

```


## Compatibility

MCU                | Work Well | Work Wrong | Untested  | Remarks
------------------ | :----------: | :----------: | :---------: | -----
Arduino uno |       √      |             |            | 
FireBeetle esp32 |       √      |             |            | 


## History

- data 2020-12-18
- version V1.0


## Credits

·Written by [yangfeng]<fary_young@outlook.com>,2020,(Welcome to our [website](https://www.dfrobot.com/))
