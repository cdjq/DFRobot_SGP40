/*!
 * @file getVocIndexRhT.ino
 * @brief 读取环境voc指数，范围是0-500;本示例中需输入环境温湿度进行校准。
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
    delay(1000); /* 等待1秒*/
  }
  //sgp.getSerial();//返回3个序列号
  //Serial.println("initialization successful");
}

/* Run one measurement per second */
void loop() {
  
  //输入环境温湿度进行校准，可以得到更加精确的voc测量结果
  sgp.setRhT(/*relativeHumidityRH = */ 48,/*temperatureC = */ 22);
  
  //串口打印voc指数
  Serial.print("voc指数为：");
  Serial.println(sgp.getVocIndex());
  delay(1000);//延迟一秒进行下次测量打印
}
