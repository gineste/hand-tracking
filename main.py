#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PatternObserverClass import *
from ServoSerialConnectionClass import *
from HandRecognitionClass import *

myservo = ServoSerialConnectionClass(name="DSSERVO_20kg", verbose=True)


hand_recognition_thread = HandRecognitionClass(name="hand_reco_01")
hand_recognition_thread.start()
hand_recognition_thread.register(myservo)

print("here1")
myservo.start()
print("here2")
