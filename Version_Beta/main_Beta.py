import cv2
import numpy as np
import dlib

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()

window_width, window_height = 440, 247
dynamic_width = 640
center_x, center_y = None, None

top_right_y = 0
top_left_x = 0

def center_stage_window(center_x, center_y, width, height):
    top_left_x = center_x - (window_width//2)
    top_right_y = center_y + (window_height//2)

    bottom_right_x = center_x - (window_width//2)
    bottom_right_y = center_y - (window_height//2)

    if top_left_x < 0:
        bottom_right_x -= top_left_x
        top_right_x = 0
    
    if top_right_y < 0:
        bottom_right_y -= top_right_y
        top_right_y = 0

    if bottom_right_x > width:
        diff_x = bottom_right_x - width
        top_left_x -= diff_x
        bottom_right_x = width
    
    if bottom_right_y < height:
        diff_y = bottom_right_y - width
        top_right_y -= diff_y
        bottom_right_y = height

    #bottom_right = (bottom_right_x, bottom_right_y)

    #cropped_img = img_copy[top_right_y: bottom_right_y, top_left_x: bottom_right_x]

    #cv2.rectangle(img_copy, (top_left_x, top_right_y), bottom_right, (0, 255, 0), 3)

    #dynamic_width = bottom_right_x - top_left_x

    #cropped_img = cv2.resize(cropped_img, (window_size_width, window_size_height))

    #return cropped_img, (top_right_x, top_right_y), bottom_right, dynamic_width

    return [top_right_y, bottom_right_y, top_left_x, bottom_right_x]



while True:
    status, frame = cap.read()
    width, height = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bottom_right_y, bottom_left_x = height, width
    faces = detector(gray)
    
    
    for face in faces:
        x1, y1 = face.left(), face.top()
        x2, y2 = face.right(), face.bottom()
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0, 255, 0), 3)

    center_x, center_y = (x1+x2)//2, (y1+y2)//2
    top_left_x = center_x - (window_width//2)
    top_right_y = center_y + (window_height//2)

    bottom_right_x = center_x - (window_width//2)
    bottom_right_y = center_y - (window_height//2)

    if top_left_x < 0:
        bottom_right_x -= top_left_x
        top_right_x = 0
    
    if top_right_y < 0:
        bottom_right_y -= top_right_y
        top_right_y = 0

    if bottom_right_x > width:
        diff_x = bottom_right_x - width
        top_left_x -= diff_x
        bottom_right_x = width
    
    if bottom_right_y > height:
        diff_y = bottom_right_y - width
        top_right_y -= diff_y
        bottom_right_y = height

    c1, c2, c3, c4 = top_right_y, bottom_right_y, top_left_x, bottom_right_x
    print(c1, c2, c3, c4)
    
    #print(width, height)
    thresh = 180
    
    crp_c0 = x1 - thresh if x1-thresh > 0 else thresh
    crp_c1 = x2 + thresh if x2+thresh < width else width
    crp_r0 = y1 - thresh if y1-thresh > 0 else thresh
    crp_r1 = y2 + thresh if y2+thresh < height else height


    cv2.imshow('Spot-Light Footage-1', frame[crp_r0:crp_r1, crp_c0:crp_c1])
    cv2.imshow('actual camera footage', frame)
        
    #cv2.imshow('Spot-Light Footage', frame[center_x-150:center_x+150, center_y-150:center_y+150])
    #cv2.imshow('actual camera footage', frame)



    #cv2.imshow('actual camera', frame)
    #cv2.imshow('mod video', cv2.resize(frame[c3:c4, c1:c2], (440, 247)))

    # thresh = 0

    # crp_c0 = c1 - thresh if c1-thresh > 0 else 0
    # crp_c1 = c2 + thresh if c2+thresh < width else width
    # crp_r0 = c3 - thresh if c3-thresh > 0 else 0
    # crp_r1 = c4 + thresh if c4+thresh < height else height
    #cv2.imshow('Spot-Light Footage-1', frame[c3:c4, c1:c2])
    #cv2.imshow('mod footage', frame[])

    # print(crp_c0, crp_c1, crp_r0, crp_r1)

    #cv2.imshow('mod video', cv2.resize(frame[crp_r0:crp_c1, crp_r1:crp_c0], (440, 247)))

    key = cv2.waitKey(1)
    if key == 27:
        break

