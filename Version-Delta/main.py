import cv2
import numpy as np
import dlib

cap = cv2.VideoCapture(0)
#face_cascade = cv2.CascadeClassifier('Version_Alpha/haarcascade_frontalface_default.xml')
detector = dlib.get_frontal_face_detector()


# dynamic_width = window_width
center_x, center_y = None, None

top_left_y = 0
top_left_x = 0
bottom_right_y = 0
bottom_right_x = 0

def spot_light_window(center_x, center_y, width, height, window_width, window_height):
    # window_width, window_height = 640, 360
    top_left_x = center_x - (window_width//2)
    top_left_y = center_y - (window_height//2)

    bottom_right_x = center_x + (window_width//2)
    bottom_right_y = center_y + (window_height//2)

    if top_left_x < 0:
        top_left_x = 0
        bottom_right_x = window_width

    if top_left_y < 0:
        top_left_y = 0
        bottom_right_y = window_height

    if bottom_right_x > width:
        bottom_right_x = width
        top_left_x = width - window_width

    if bottom_right_y > height:
        bottom_right_y = height
        top_left_y = height - window_height

    return [top_left_x, top_left_y, bottom_right_x, bottom_right_y]

while True:
    status, frame = cap.read()
    width, height = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    x1, y1, x2, y2 = 0, 0, 0, 0
    n = len(faces)
    if len(faces) <= 1:
        for face in faces:
            x1, y1 = face.left(), face.top()
            x2, y2 = face.right(), face.bottom()
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0, 255, 0), 2)
    else:
        face_cords = []
        for face in faces:
            x1, y1 = face.left(), face.top()
            x2, y2 = face.right(), face.bottom()
            face_cords.append((x1, y1, x2, y2))
        x, y = 0, 0
        minx, maxy, maxx, miny = 10000, 0, 0, 10000
        for ele in face_cords:
            x += (ele[0]+ele[2])//2
            y += (ele[1]+ele[3])//2
            minx = min(minx, ele[0])
            maxy = max(maxy, ele[3])
            maxx = max(maxx, ele[2])
            miny = min(miny, ele[1])
        x, y = x//n, y//n         
        mul = 1
        while True:
            left = x-mul*16
            right = x+mul*16
            top = y-mul*9
            bottom = y+mul*9
            if left < minx and right > maxx and top < miny and bottom > maxy:
            #     if left < 0:
            #         right+=(-left)
            #         left = 0
            #     if top < 0:
            #         bottom+=(-top)
            #         top = 0
            #     if right > 1280:
            #         left-=(right-1280)
            #         right = 1280
            #     if bottom > 720:
            #         top 
            #         bottom = 0
                x1, y1, x2, y2 = left, top, right, bottom
                break
            else:
                mul+=1
        
    
    # for face in faces:
    #     x1, y1 = face.left(), face.top()
    #     x2, y2 = face.right(), face.bottom()
        #cv2.rectangle(frame, (x1,y1), (x2,y2), (0, 255, 0), 1)
    tlx, tly, brx, bry = spot_light_window((x1+x2)//2, (y1+y2)//2, 1280, 720, max(x2-x1, 640), max(y2-y1, 360))
    cv2.rectangle(frame,(tlx,tly),(brx,bry),(0,255,0),2)
    print("frame coords: ", end = "")
    print(tlx, tly, brx, bry)
    print("center coords: ", end = "")
    print(x1, y1, x2, y2)

    #print(width, height)
    # thresh = 180

    # crp_c0 = x1 - thresh if x1-thresh > 0 else thresh
    # crp_c1 = x2 + thresh if x2+thresh < width else width
    # crp_r0 = y1 - thresh if y1-thresh > 0 else thresh
    # crp_r1 = y2 + thresh if y2+thresh < height else height


    cv2.imshow('Spot-Light Footage-1', cv2.resize(frame[tly+2:bry-2, tlx+2:brx-2], (640, 360)))
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
    # cv2.imshow('Spot-Light Footage-1', frame[c3:c4, c1:c2])
    # cv2.imshow('mod footage', frame[])

    # print(crp_c0, crp_c1, crp_r0, crp_r1)

    #cv2.imshow('mod video', cv2.resize(frame[crp_r0:crp_c1, crp_r1:crp_c0], (440, 247)))

    key = cv2.waitKey(1)
    if key == 27:
        break
