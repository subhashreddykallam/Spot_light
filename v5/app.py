import cv2
import numpy as np
import dlib
import mediapipe as mp
from package.spotlight_frame import spotlight_frame
from package.handle_single_face import handle_single_face
from package.handle_multi_face import handle_multi_face

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

resolution = {360: [640, 360], 480: [852, 480]}
sf_width, sf_height = resolution[480]

top, left, bottom, right = 0, 0, 0, 0

while True:
    status, frame = cap.read()
    height, width = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    co_ords = []
    n = len(faces)
    if len(faces) <= 1:
        co_ords = handle_single_face(faces)
    else:
        co_ords = handle_multi_face(faces)
    print(co_ords)
    left, top, right, bottom = co_ords
    sf_left, sf_top, sf_right, sf_bottom = spotlight_frame((left+right)//2, (top+bottom)//2, width, height, max(right-left, sf_width), max(bottom-top, sf_height))
    cv2.rectangle(frame,(sf_left,sf_top),(sf_right,sf_bottom),(0,255,0),2)

    cv2.imshow('Spotlight', cv2.resize(frame[sf_top+2:sf_bottom-2, sf_left+2:sf_right-2], (sf_width, sf_height)))
    cv2.imshow('Webcam', frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
