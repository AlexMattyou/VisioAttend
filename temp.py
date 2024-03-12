import os
import cv2
from time import sleep

rootLoc = os.path.dirname(os.path.realpath(__file__))

def capture(port=0, interval=60, imageNumber=0):
    cap = cv2.VideoCapture(port)
    success, frame = cap.read()
    if success:
        imageNumber += 1
        print("Running")
        cv2.imwrite(rootLoc + "\\images\\captured\\" + f"{imageNumber}.png", frame)
    cap.release()
    sleep(interval)
    capture(port, interval, imageNumber)
    
capture()