import cv2
import mediapipe as mp
import time
import math
try:
    import RPi.GPIO as GPIO
    rasp = True
except:
    rasp = False
    print("on dirait qu'on n'est pas sur un raspberry ici... pas de GPIO!")

# pip3 install opencv-contrib-python
# pip3 install mediapipe-rpi4
# pip3 install RPI.GPIO


cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1,
                      min_detection_confidence=0.75,
                      min_tracking_confidence=0.95)
mpDraw = mp.solutions.drawing_utils
mpDraw.draw_landmarks
pin1 = 38
pin2 = 37
if rasp:
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

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:

            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                z_distance_offset = -0.005
                cx, cy, cz = int(lm.x * w), int(lm.y * h), -1 / (lm.z+z_distance_offset)
                # print(id, cx, cy)
                if id == 4:
                    print(id, cx, cy, int(cz))
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    thumb_x = cx
                    thumb_y = cy
                if id == 8:
                    print(id, cx, cy, int(cz))
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    little_x = cx
                    little_y = cy
            # compute distance between fingers and apply FoV depth correction:
            dist = math.sqrt((thumb_x - little_x)**2 + (thumb_y - little_y)**2) * cz
            print(dist)
            print("\n")

            # la lED :
            if rasp:
                if (math.sqrt((thumb_x - little_x) ** 2 + (thumb_y - little_y) ** 2) < 500):
                    GPIO.output(pin1, GPIO.LOW)
                    GPIO.output(pin2, GPIO.HIGH)
                else:
                    GPIO.output(pin1, GPIO.HIGH)
                    GPIO.output(pin2, GPIO.LOW)

            # dessiner les points de la main et les liens entre eux.
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.putText(img, str(int(dist)), (10, 170), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    # full screen!:
    cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("window", img)
    c = cv2.waitKey(1)
    if c == 27:  # escape to exit
        break
        cv2.destroyAlqlWindows()
