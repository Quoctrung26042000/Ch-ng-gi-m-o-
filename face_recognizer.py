import cv2
import numpy as np
from PIL import Image
import os
import config
import process_database

# eye blink detection
from imutils.video import VideoStream
import time
import f_detector
import imutils

# eye blink detection
detector_2 = f_detector.eye_blink_detector()

COUNTER = 0
TOTAL = 0
#***************

### Let's go!
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')

face_cascade_Path = "haarcascade_frontalface_default.xml"


faceCascade = cv2.CascadeClassifier(face_cascade_Path)

font = cv2.FONT_HERSHEY_SIMPLEX


names = config.names

#Video Capture
cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)
# Min Height and Width for the  window size to be recognized as a face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)
while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        # COUNTER,TOTAL = detector_2.eye_blink(gray,cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2),COUNTER,TOTAL)

        # detectar_rostro
        rectangles_2 = detector_2.detector_faces(gray, 0)
        boxes_face = f_detector.convert_rectangles2array(rectangles_2, img)
        if len(boxes_face) != 0:
            # seleccionar el rostro con mas area
            areas = f_detector.get_areas(boxes_face)
            index = np.argmax(areas)
            rectangles_2 = rectangles_2[index]
            boxes_face = np.expand_dims(boxes_face[index], axis=0)
            # blinks_detector
            COUNTER, TOTAL = detector_2.eye_blink(gray, rectangles_2, COUNTER, TOTAL)
            # print("couter blinks: ", COUNTER)
            print("total blinks:", TOTAL)
            if (TOTAL  > 0 and confidence < 53):
                # if (confidence < 70):
                id = names[id]
                confidence_1 = "Real: {0}%".format(round(100 - confidence))
                print(confidence_1)
                confidence = "Welcome!"
            else:
                # Unknown Face
                id = "Who are you ?"
                confidence_1 = "Real: {0}%".format(round(100 - confidence))
                print(confidence_1)
                confidence = "Please recheck!"

        cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

    cv2.imshow('camera', img)
    # Escape to exit the webcam / program
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break
print("\n [INFO] Exiting Program.")
cam.release()
cv2.destroyAllWindows()


