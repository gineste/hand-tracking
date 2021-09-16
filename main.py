#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Code pour faire tourner le servomoteur via une communication série Arduino.

from ServoSerialConnectionClass import *
from HandRecognitionClass import *

# création de l'instance Servo
myservo = ServoSerialConnectionClass(name="DSSERVO.20kg_handler", verbose=True, angle_range=(10, 90), baudrate=9600)

# création de l'instance de reconnaissance de main
hand_recognition_thread = HandRecognitionClass(name="hand_reco_01", verbose=False, resize_ratio=1, camera_id=1)


# On démarre la boucle du servomoteur. On envoie un angle en port série,
# on attent (0.5sec) qu'arduino renvoie le callback pour envoyer une nouvelle commande.
myservo.start()


# on abonne le handler du servo aux updates de la reconnaissance de main
# a chaque update la valeur de la propriété `current_angle` sera modifiée
hand_recognition_thread.register(myservo)
hand_recognition_thread.start()



