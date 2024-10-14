/*
That code is not working on visual studio code or any other IDE that code working only arduino IDE
*/

// Pin definitions
const int ENA = 6;  // PWM pin to control motor speed
const int IN1 = 3;   // Motor driver IN1 pin
const int IN2 = 5;  // Motor driver IN2 pin

String StrSpeed = ("");
int speed = 0;

void setup() {

  //define pinmodes
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  //set serial
  Serial.begin(9600);
  //wait for set serial
  while(!Serial);

  //check arduino & python connection
  if(Serial.available()>0){
    char received = Serial.read();
    if(received == '1'){
      Serial.println("Received 1");
    }
  }
}

void loop() {

}