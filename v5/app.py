import cv2
import numpy as np
import dlib
import tensorflow as tf
import os, sys
import argparse
import pyvirtualcam
from pyvirtualcam import PixelFormat
from package.spotlight_frame import spotlight_frame
from package.handle_single_face import handle_single_face
from package.handle_multi_face import handle_multi_face
from package.super_resolution import super_resolution
from package.get_center_frame import get_center_frame

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
resolution = {360: (640, 360), 480: (852, 480), 720: (1280, 720), 1080: (1920, 1080)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--res', type=int, help='Resolution to use from the webcam input', default=480)
    parser.add_argument('--scale', type=int, help='Scaling factor of the model', default=2)
    args = parser.parse_args()

    scale = args.scale
    if scale > 4 or scale < 2:
        print("Upscale factor scale is not supported. Choose 2, 3 or 4.")
        exit()

    config = tf.compat.v1.ConfigProto()
    config.gpu_options.allow_growth = True

    super_resolution = super_resolution(config, scale)

    sf_width, sf_height = resolution[args.res]
    top, left, bottom, right = 0, 0, 0, 0
    
    prev_center = [-1, -1]
    sf_left, sf_top, sf_right, sf_bottom = 0, 0, 0, 0
    def center(x1, y1, x2, y2):
        return [(x1+x2)//2, (y1+y2)//2]

    def displacement(p, q):
        return abs(p[0]-q[0]) + abs(p[1]-q[1])
      
    with pyvirtualcam.Camera(640, 360, 30, fmt=PixelFormat.BGR) as cam:
        while True:
            status, frame = cap.read()
            if not status:
                print("Error reading")
                continue
            frame_height, frame_width = frame.shape[:2]
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)

            co_ords = get_center_frame(frame_width, frame_height, sf_width, sf_height)

            n = len(faces)
            if len(faces) <= 1:
                co_ords = handle_single_face(faces, co_ords)
            else:
                co_ords = handle_multi_face(faces, co_ords)
            left, top, right, bottom = co_ords
            c = center(left, top, right, bottom)
            img = []

            if prev_center == [-1, -1]:
                prev_center = c
                sf_left, sf_top, sf_right, sf_bottom = spotlight_frame((left+right)//2, (top+bottom)//2, frame_width, frame_height, max(right-left, sf_width), max(bottom-top, sf_height))
            else:
                x_delta = c[0] - prev_center[0]
                y_delta = c[1] - prev_center[1]
                if abs(x_delta) > 30 or abs(y_delta) > 30:
                    if x_delta!=0:
                        sf_left+=(x_delta//abs(x_delta))*4
                        sf_right+=(x_delta//abs(x_delta))*4
                    if y_delta!=0:
                        sf_top+=(y_delta//abs(y_delta))*4
                        sf_bottom+=(y_delta//abs(y_delta))*4
                    sf_left, sf_top, sf_right, sf_bottom = spotlight_frame((left+right)//2, (top+bottom)//2, frame_width, frame_height, max(right-left, sf_width), max(bottom-top, sf_height))
                    prev_center = c

            img = frame[sf_top:sf_bottom, sf_left:sf_right]
            img = cv2.resize(img, (640, 360), interpolation=cv2.INTER_AREA)

            cv2.rectangle(frame,(sf_left,sf_top),(sf_right,sf_bottom),(0,255,0),2)

#             cv2.imshow('Processed image', super_resolution.upscale(img))
#             cv2.imshow('Raw Webcam', frame)
            cam.send(super_resolution.upscale(img))
            cam.sleep_until_next_frame()

            key = cv2.waitKey(1)
            if key == 27:
                break
