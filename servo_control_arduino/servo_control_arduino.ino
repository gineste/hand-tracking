// Include the Servo Library
#include <Servo.h>


// Create a Servo object
Servo myservo; // le servo DSSERVO 20Kg va de 70° à 160° lorsqu'il est monté sur la pince. (70° = ouvert à fond)
int position = 0;
String readString;

void setup()
{
   // Attach servo on pin 9 to the servo object
  myservo.attach(9);
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  myservo.write(100);
}


void loop()
{

  while (Serial.available()) {
    char c = Serial.read();  //gets one byte from serial buffer
    readString += c; //makes the String readString
    delay(2);  //slow looping to allow buffer to fill with next character
  }

  if (readString.length() >0) {
    int n = readString.toInt();  //convert readString into a number
    myservo.write(n);
    analogWrite(LED_BUILTIN, 255);
    delay(n);
    analogWrite(LED_BUILTIN, 0);
    delay(n);
    analogWrite(LED_BUILTIN, 255);
    delay(n);
    analogWrite(LED_BUILTIN, 0);
    delay(n);
    readString="";
  } 

}
