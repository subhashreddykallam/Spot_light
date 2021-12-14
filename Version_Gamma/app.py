from flask import Flask, render_template, Response

import cv2
import numpy as np
import dlib
import os

detector = dlib.get_frontal_face_detector()
global cap
cap = cv2.VideoCapture(0)
cap.release()

def spot_light_window(center_x, center_y, width, height):
    window_width, window_height = 640, 360
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

def activate_Spotlight():
    global cap
    cap = cv2.VideoCapture(0)
    while True:
        status, frame = cap.read()
        if not status:
            print("Some issue")
        width, height = 1280, 720
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        
        for face in faces:
            x1, y1 = face.left(), face.top()
            x2, y2 = face.right(), face.bottom()
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0, 255, 0), 2)
        if len(faces) == 0:
            tlx, tly, brx, bry = spot_light_window((width)//2, (height)//2, width, height)
        else:
            tlx, tly, brx, bry = spot_light_window((x1+x2)//2, (y1+y2)//2, width, height)

        # print(tlx, tly, brx, bry)
        ret, buffer = cv2.imencode('.jpg', cv2.flip(frame[tly:bry, tlx:brx], 1))
        image = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')

app = Flask(__name__)

def closeCam():
    if cap.isOpened():
        cap.release()

@app.route('/')
@app.route('/index')
def index():
    closeCam()
    return render_template('index.html')

@app.route('/video_page')
def video_page():
    closeCam()
    return render_template('video_page.html')

@app.route('/about')
def about():
    closeCam()
    return render_template('about.html')

@app.route('/spotlight_feed')
def spotlight_feed():
    return Response(activate_Spotlight(), mimetype='multipart/x-mixed-replace; boundary=frame')

registry = os.path.join('static', 'Images')

if __name__ == '__main__':
    app.run(debug=True)