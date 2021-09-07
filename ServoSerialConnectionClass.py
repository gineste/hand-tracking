#!/usr/bin/env python3
# -- coding: utf-8 --
import time
import threading
from threading import Thread
from PatternObserverClass import *
import serial
import sys
import glob
import serial


# Fonction qui cherche les ports séries disponibles. On prendra le premier de la liste! Windows ou Linux
def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


# fonction équivalent au map() sur arduino
def map_custom(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    toreturn_unbound = rightMin + (valueScaled * rightSpan)
    if rightMax > rightMin:
        toreturn_bounded = min(rightMax, max(rightMin, toreturn_unbound))
    else:
        toreturn_bounded = min(rightMin, max(rightMax, toreturn_unbound))
    return int(toreturn_bounded)


# l'objet Servo est un thread observer.
class ServoSerialConnectionClass(Observer, Thread):
    def __init__(self, name, baudrate=9600, port="auto", angle_range=(70, 155), verbose=False):  # ex: 12
        Thread.__init__(self)
        self.name = name
        self.verbose = verbose
        self.baudrate = baudrate
        self.angle_range = angle_range
        self.current_angle = int((angle_range[0] + angle_range[1])/2)
        print("angle initi = {}".format(self.current_angle))
        if port == "auto":
            self.port = serial_ports()[0]
        else:
            self.port = port
        self.servo_connection = serial.Serial(baudrate=self.baudrate, port=self.port)

    def loop_and_wait_for_callback_arduino(self):
        while True:
            self.servo_connection.write(str(self.current_angle).encode())
            reached_position = str(self.servo_connection.readline()) # environ 500ms de délai
            print(reached_position)

    def update(self, news: ObservableData):
        self.current_angle = map_custom(news.value, 0, 1, self.angle_range[1], self.angle_range[0])
        if self.verbose: print("{} received {}, converted to {}, from {}".format(self.name, news.value, self.current_angle, news.from_who))

    def run(self):
        time.sleep(2) # pour raison inconnue, si on fait pas ca, ca foire (le terminal série n'est pas pret)
        self.loop_and_wait_for_callback_arduino()


if __name__ == "__main__":
    myservo = ServoSerialConnectionClass(name="DSSERVO_20kg", verbose=True)
    myservo.start()
