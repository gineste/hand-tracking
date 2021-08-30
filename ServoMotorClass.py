#!/usr/bin/env python3
#-- coding: utf-8 --
import RPi.GPIO as GPIO
import time
from threading import Thread


class ServoMotorClass(Thread):
    def __init__(self, pwm_gpio): # ex: 12
        Thread.__init__(self)
        GPIO.setmode(GPIO.BOARD) #Use Board numerotation mode
        GPIO.setwarnings(False) #Disable warnings
        self.pwm_gpio = pwm_gpio
        self.frequency = 50
        GPIO.setup(pwm_gpio, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pwm_gpio, self.frequency)
        self.is_servo_ready = True

    #Set function to calculate percent from angle
    def angle_to_percent(self, angle) :
        if angle > 180 or angle < 0 :
            return False
        start = 2.7
        end = 12.5
        ratio = (end - start)/180 #Calcul ratio from angle to percent
        angle_as_percent = angle * ratio
        return start + angle_as_percent

    def stop(self):
        self.pwm.stop()
        GPIO.cleanup()

    def start(self, angle=0):
        self.is_servo_ready = False
        self.pwm.start(self.angle_to_percent(angle))
        time.sleep(0.3)
        self.is_servo_ready = True

    def goto_angle(self, angle):
        self.is_servo_ready = False
        self.pwm.ChangeDutyCycle(self.angle_to_percent(angle))
        #time.sleep(0.3)
        self.is_servo_ready = True

    def goto_percent(self, percent):
        self.is_servo_ready = False
        self.pwm.ChangeDutyCycle(self.angle_to_percent(percent*180/100))
        print("servo moving!")
        #time.sleep(0.3)
        self.is_servo_ready = True
    
    def run(self):
        print("running")

    def is_ready(self):
        return self.is_servo_ready

if __name__ == "__main__":
    myservo = ServoMotorClass(12)
    # motion in percent
    myservo.start()
    for _ in range(2):
        time.sleep(0.25)
        for step in range(0, 11):
            print(step/10)
            myservo.goto_percent(percent=int(step*10))
            #time.sleep(0.2)
        print("done")
    myservo.stop()
    time.sleep(1)
