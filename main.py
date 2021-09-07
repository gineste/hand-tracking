#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Code pour faire tourner le servomoteur via une communication série Arduino.

from ServoSerialConnectionClass import *
from HandRecognitionClass import *

# création de l'instance Servo
myservo = ServoSerialConnectionClass(name="DSSERVO.20kg_handler", verbose=True)

# création de l'instance de reconnaissance de main
hand_recognition_thread = HandRecognitionClass(name="hand_reco_01", verbose=True, resize_ratio=0.5)

# on abonne le handler du servo aux updates de la reconnaissance de main
# a chaque update la valeur de la propriété `current_angle` sera modifiée
hand_recognition_thread.register(myservo)
hand_recognition_thread.start()

# On démarre la boucle du servomoteur. On envoie un angle en port série,
# on attent (0.5sec) qu'arduino renvoie le callback pour envoyer une nouvelle commande.
myservo.start()
