// Include the Servo Library
#include <Servo.h>

// Create a Servo object
Servo myservo; // le servo DSSERVO 20Kg va de 70° à 160° lorsqu'il est monté sur la pince. (70° = ouvert à fond)
int newPosition = 0;
String inByteReceivedCommand;

void setup()
{
  myservo.attach(9);
  Serial.begin(9600);
  myservo.write(100);
}

void loop()
{
  if (Serial.available()) 
  {
    inByteReceivedCommand = Serial.readStringUntil("\n");
    newPosition = inByteReceivedCommand.toInt();
    myservo.write(newPosition);
    delay(500);
    Serial.print("Servo has reached position: ");
    Serial.println(inByteReceivedCommand);
  }
}
