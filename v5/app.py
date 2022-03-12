import cv2
import numpy as np
import dlib
import tensorflow as tf
import os, sys
import argparse
from package.spotlight_frame import spotlight_frame
from package.handle_single_face import handle_single_face
from package.handle_multi_face import handle_multi_face
from package.super_resolution import super_resolution

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
available_resolutions = {360: [640, 360], 480: [852, 480]}

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

    sf_width, sf_height = available_resolutions[args.res]

    top, left, bottom, right = 0, 0, 0, 0

    while True:
        status, frame = cap.read()
        if not status:
            print("Error reading")
            continue
        height, width = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        co_ords = []
        n = len(faces)
        if len(faces) <= 1:
            co_ords = handle_single_face(faces)
        else:
            co_ords = handle_multi_face(faces)
        left, top, right, bottom = co_ords
        sf_left, sf_top, sf_right, sf_bottom = spotlight_frame((left+right)//2, (top+bottom)//2, width, height, max(right-left, sf_width), max(bottom-top, sf_height))
        img = frame[sf_top:sf_bottom, sf_left:sf_right]
        cv2.rectangle(frame,(sf_left,sf_top),(sf_right,sf_bottom),(0,255,0),2)
        cv2.imshow('Super-resolution', cv2.resize(super_resolution.upscale(frame[sf_top+2:sf_bottom-2, sf_left+2:sf_right-2]), (1280, 720)))
        # cv2.imshow('Webcam', frame)

        key = cv2.waitKey(1)
        if key == 27:
            break
