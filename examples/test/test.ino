/*!
 * @file getVocIndex.ino
 * @brief 读取环境voc指数，范围是0-500
 * @n 实验现象：每秒读取一次环境voc指数，并打印到串口
 *
 * @copyright	Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @licence     The MIT License (MIT)
 * @author wangyanfang<yanfang.wang@dfrobot.com>
 * @version  V1.0
 * @date  2020-12-3
 * @url  
 */
#include <DFRobot_SGP40.h>

DFRobot_SGP40 sgp;

void setup() {
  Serial.begin(115200);  // start serial for output
  
  while (sgp.begin()) {
    Serial.println("initialization failed: ");
    delay(1000); /* wait one second */
  }
  sgp.getSerial();//返回3个序列号
  Serial.println("initialization successful");
}

/* Run one measurement per second */
void loop() {
  
}
