
#include <SPI.h>
#include <ArduinoJson.h>
#include "RH_RF95.h"

#define RFM95_CS 10
#define RFM95_RST 4
#define RFM95_INT 2
#define RF95_FREQ 433.0
#define RF95_PREMABLE_LENGTH 8

#define SENSOR_PIN A2 //土壤湿度传感器adc引脚
int sensorValue = 0;
int sensorPowerCtrlPin = 5;

//Lora芯片对象
RH_RF95 rf95(RFM95_CS, RFM95_INT);

void setup()
{
  Serial.begin(115200);

  pinMode(sensorPowerCtrlPin, OUTPUT);

  //重启
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  //初始化
  while (!rf95.init())
  {
    Serial.println("LoRa radio init failed");
    while (1)
      ;
  }
  Serial.println("LoRa radio init OK!");

  //设置频率
  if (!rf95.setFrequency(RF95_FREQ))
  {
    Serial.println("setFrequency failed");
    while (1)
      ;
  }
  Serial.print("Set Freq to: ");
  Serial.println(RF95_FREQ);

  //设置发射功率
  rf95.setTxPower(23, false);

  //设置前导码长度
  rf95.setPreambleLength(RF95_PREMABLE_LENGTH);
  Serial.print("Set setPreambleLength to: ");
  Serial.println(RF95_PREMABLE_LENGTH);

  //rf95.printRegisters();

  digitalWrite(sensorPowerCtrlPin, HIGH);
}

//土壤传感器代码
void loop()
{ 
  sensorValue = analogRead(SENSOR_PIN);
  String temp = String(sensorValue);
  Serial.println(sensorValue);
  String message = "SOIL" + temp;
  Serial.println(message);

  // Send a message to rf95_server
  uint8_t radioPacket[message.length() + 1];
  message.toCharArray(radioPacket, message.length() + 1);
  radioPacket[message.length() + 1] = '\0';
  Serial.println("Sending...");
  delay(10);
  rf95.send((uint8_t *)radioPacket, message.length() + 1);

  delay(3000); //unit: ms
}