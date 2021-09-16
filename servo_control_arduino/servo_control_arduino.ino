// Include the Servo Library
#include <Servo.h>

// Create a Servo object
Servo myservo; // le servo DSSERVO 20Kg va de 70° à 160° lorsqu'il est monté sur la pince. (70° = ouvert à fond)
int newPosition = 0;
String inByteReceivedCommand;

void setup()
{
  Serial.begin(9600);
  delay(1000);
  myservo.write(10);
  myservo.attach(9);
  delay(500);
}

void loop()
{
  if (Serial.available()) 
  {
    delay(1);
    inByteReceivedCommand = Serial.readStringUntil("\n");
    newPosition = inByteReceivedCommand.toInt();
    // do some checks:
    if (newPosition < 0 || newPosition > 180){
      Serial.println("discarded 1 invalid position");
    } else {
      myservo.write(newPosition);
      delay(650);
      //Serial.print("Servo has reached position: ");
      Serial.print(inByteReceivedCommand);
      Serial.print("\n");
    }
  }
  /*
  for (int i=0; i<255; i++){
    newPosition += 10;
    if (newPosition > 90){
      newPosition=0;
    }
    Serial.println(newPosition);
    myservo.write(newPosition);
    delay(2000);
  }
 */
}
