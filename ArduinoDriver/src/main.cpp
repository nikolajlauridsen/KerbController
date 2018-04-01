#include <Arduino.h>
#define StageLight 13
#define StageBtn 2
#define Throttle A0
#define YAW A1
#define PITCH A2
#define SAS 3
#define SAS_INDI 12
#define ThrottleCorrect 500
#define ThrottleCutoff 8
/*
5.1k values
correct = 335
cutoff = 10
*/

void setup() {
  // Set up IO
  pinMode(StageLight, OUTPUT);
  pinMode(SAS_INDI, OUTPUT);
  digitalWrite(StageLight, LOW);
  digitalWrite(SAS_INDI, LOW);
  pinMode(StageBtn, INPUT);
  pinMode(Throttle, INPUT);
  pinMode(SAS, INPUT);
  Serial.begin(9600);
  digitalWrite(StageLight, HIGH);
}

bool stageState = false;
bool stageHigh = false;
bool sasState = false;
bool sasOn = false;
unsigned int throttleSens = 5;
unsigned int throttleValue;
float throttleFactor;
float prevThrottle;
unsigned int yaw;
unsigned int pitch;
unsigned int prevYaw;
unsigned int prevPitch;
void loop() {
  // Buttons
  stageHigh = digitalRead(StageBtn);
  if(stageHigh){
    if(!stageState){
      Serial.println("go");
      stageState = true;
    }
  } else {
    stageState = false;
  }

  if(digitalRead(SAS)){
      if(!sasState){
          Serial.println("sas");
          sasState = true;
          if(sasOn){
              sasOn = false;
              digitalWrite(SAS_INDI, LOW);
          } else {
              sasOn = true;
              digitalWrite(SAS_INDI, HIGH);
          }
      }
  } else {
      sasState = false;
  }

  // Throttle
  throttleValue = analogRead(Throttle);
  throttleValue -= ThrottleCorrect;
  if(throttleValue < ThrottleCutoff){
      throttleValue = 0;
  }
  throttleFactor = throttleValue / 523.0;
  int throttleperc = round(throttleFactor*100);
  if (throttleperc != prevThrottle){
      Serial.print("t:");
      Serial.println(throttleperc);
      prevThrottle = throttleperc;
  }

  // Pitch/YAW
  yaw = analogRead(YAW);
  pitch = analogRead(PITCH);
  if(yaw != prevYaw or pitch != prevPitch){
      Serial.print("c:");
      Serial.print(yaw);
      Serial.print(",");
      Serial.println(pitch);
      prevPitch = pitch;
      prevYaw = yaw;
  }

  delay(200);
}
