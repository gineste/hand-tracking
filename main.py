import cv2
import mediapipe as mp
import time
import math
from ServoMotorClass import *
try:
    import RPi.GPIO as GPIO
    rasp = True
except:
    rasp = False
    print("on dirait qu'on n'est pas sur un raspberry ici... pas de GPIO!")

# pip3 install opencv-contrib-python
# pip3 install mediapipe-rpi4
# pip3 install RPI.GPIO

# lancer la capture et sur une première capture récupérer les dimensions de l'image.
videocapture = cv2.VideoCapture(0)
_, frame = videocapture.read()
h, w, c = frame.shape

# start servomotor
myservo = ServoMotorClass(12)
myservo.start()

# resizing parameters
resize_ratio = 0.3
resize_width = int(w*resize_ratio)
resize_height = int(h*resize_ratio)

mpHands = mp.solutions.hands
drawingModule = mp.solutions.drawing_utils
hands = mpHands.Hands(max_num_hands=1,
                      min_detection_confidence=0.75,
                      min_tracking_confidence=0.95)
mpDraw = mp.solutions.drawing_utils
mpDraw.draw_landmarks
if rasp:
    pin1 = 38
    pin2 = 37
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.output(pin1, GPIO.HIGH)
    GPIO.output(pin2, GPIO.LOW)

pTime = 0
cTime = 0
thumb_x = 0
thumb_y = 0
little_x = 0
little_y = 0
dist = 0
previous_valid_depth = None
correction_factor_hand_z_1 = 150
correction_factor_hand_z_2 = 0.8

def checked_depth_mm(depth):
    depth = min(3000, max(1, depth))
    return round(depth)

def compute_depth_cm(finger1, finger2):
    average_depth = (finger1.z + finger2.z)/2
    distance_cm = -1.32 + 7.2298*(1/(0.03-average_depth))
    return round(max(0, distance_cm))
move_number=0
########### BOUCLE de calcul et d'affichage
while True:
    success, img = videocapture.read()
    # resize image
    img_resized = cv2.resize(img, (resize_width, resize_height), interpolation=cv2.INTER_NEAREST)
    imgRGB = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    # trouver et calculer les mains:
    results = hands.process(imgRGB)
    cv2.rectangle(img, (10, 50), (30, 200), (100, 100, 100), 3)
    # si on a une réponse (results.multi_hand_landmarks existe):

    if results.multi_hand_landmarks:
        profondeur_main = None
        # on boucle pour chaque main mais comme il n'y a qu'une main dans le paramétrage, c'est une seule fois.
        for chaque_main in results.multi_hand_landmarks:
            print("___________new hand")
            doigt_pouce = chaque_main.landmark[mpHands.HandLandmark.THUMB_TIP]
            doigt_index = chaque_main.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
            profondeur_main = compute_depth_cm(doigt_index, doigt_pouce)
            print("profondeur main cm : {}".format(profondeur_main))
            doigt_pouce_coords = drawingModule._normalized_to_pixel_coordinates(doigt_pouce.x, doigt_pouce.y, w, h)
            doigt_index_coords = drawingModule._normalized_to_pixel_coordinates(doigt_index.x, doigt_index.y, w, h)
            if doigt_index_coords and doigt_pouce_coords:
                # calculer la distance entre les 2 doigts, corrigé par la profondeur (correction approx)
                dist = math.sqrt((doigt_index_coords[1] - doigt_pouce_coords[1])**2 + (doigt_index_coords[0] - doigt_pouce_coords[0])**2)
                dist = round( dist * profondeur_main**(correction_factor_hand_z_2) / correction_factor_hand_z_1 )
                #dist = checked_depth_mm(dist)
                print("ecart doigts mm : {}".format(dist))
                cv2.circle(img, doigt_pouce_coords, 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, doigt_index_coords, 15, (255, 0, 255), cv2.FILLED)
                # dessiner les points de la main et les liens entre eux.
                mpDraw.draw_landmarks(img, chaque_main, mpHands.HAND_CONNECTIONS)
                cv2.line(img, doigt_pouce_coords, doigt_index_coords, (0, 255, 0), thickness=3, lineType=8)
                # draw gauge (le point 0,0 est en haut à gauche !! attention
                max_dist  = 25
                min_jauge = 195
                max_jauge = 55
                cur_jauge = max(max_jauge, min(min_jauge, min_jauge - dist/max_dist * (min_jauge-max_jauge)))
                cv2.rectangle(img, (15, min_jauge), (25, int(cur_jauge)), (0, 255, 0), -1)
                cv2.rectangle(img, (10, 50), (30, 200), (0, 255, 0), 3)
                cv2.putText(img, "{} cm".format(int(dist)), (35, int(cur_jauge+15)), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                myservo.goto_percent(min(100, dist/25*100))
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, "{} fps".format(int(fps)), (5, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    # full screen!:
    #cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    #cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("window", img)
    c = cv2.waitKey(1)
    if c == 27:  # escape to exit
        cv2.destroyAllWindows()
        break
