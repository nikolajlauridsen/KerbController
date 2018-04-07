#include <Arduino.h>
#include <LiquidCrystal_I2C.h>

#define StageLight 13
#define StageBtn 2
#define Throttle A0
#define YAW A1
#define PITCH A2
#define SAS 4
#define SAS_INDI 12
#define ThrottleCorrect 500
#define ThrottleCutoff 8
/*
5.1k values
correct = 335
cutoff = 10
*/

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  // Screen
  lcd.init();
  lcd.backlight();
  // Set up IO
  lcd.print("Setting up.");
  pinMode(StageLight, OUTPUT);
  pinMode(SAS_INDI, OUTPUT);
  digitalWrite(StageLight, LOW);
  digitalWrite(SAS_INDI, LOW);
  pinMode(StageBtn, INPUT);
  pinMode(Throttle, INPUT);
  pinMode(SAS, INPUT);
  Serial.begin(19200);
  digitalWrite(StageLight, HIGH);
  lcd.clear();
}

bool stageState = false;
bool stageHigh = false;
unsigned int throttleSens = 5;
unsigned int throttleValue;
float throttleFactor;
float prevThrottle;
unsigned int yaw;
unsigned int pitch;
unsigned int prevYaw;
unsigned int prevPitch;
bool prevSAS;
bool currentSAS;

void parseScreen(){
    unsigned int x, y;
    char c;
    delay(100);
    while (Serial.available() > 0){
        x = Serial.read();
        if (x == 255){
            break;
        }
        y = Serial.read();
        c = Serial.read();
        lcd.setCursor(x,y);
        lcd.write(c);
    }
}

String command = "";
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

  // SAS
  currentSAS = digitalRead(SAS);
  if(prevSAS != currentSAS){
     Serial.print("sas:");
     Serial.println(!currentSAS);
     prevSAS = currentSAS;
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

  // Read inputs from computer
  if (Serial.available() > 0){
      command = Serial.readStringUntil('\n');
  }

  // Do stuff with input
  if (command.length() > 0){
      if (command == "scr"){
          Serial.println("Setting screen.");
          parseScreen();
      }
  }

  // Reset input
  command = "";
  delay(200);
}
