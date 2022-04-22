import cv2
import numpy as np
import dlib

cap = cv2.VideoCapture(0)
#face_cascade = cv2.CascadeClassifier('Version_Alpha/haarcascade_frontalface_default.xml')
detector = dlib.get_frontal_face_detector()


dynamic_width = 640
center_x, center_y = None, None

top_left_y = 0
top_left_x = 0
bottom_right_y = 0
bottom_right_x = 0


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

    # config = tf.compat.v1.ConfigProto()
    # config.gpu_options.allow_growth = True

    # super_resolution = super_resolution(config, scale)

    sf_width, sf_height = resolution[args.res]
    top, left, bottom, right = 0, 0, 0, 0
    with pyvirtualcam.Camera(640, 360, 30, fmt=PixelFormat.BGR) as cam:
        while True:
            status, frame = cap.read()
            if not status:
                print("Error reading")
                continue
            frame_height, frame_width = frame.shape[:2]
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)
            co_ords = get_frame_center(frame_width, frame_height, sf_width, sf_height)
            n = len(faces)
            print(n)
            if len(faces) <= 1:
                co_ords = handle_single_face(faces, co_ords)
            else:
                co_ords = handle_multi_face(faces, co_ords)
            left, top, right, bottom = co_ords
            print(co_ords)
            sf_left, sf_top, sf_right, sf_bottom = spotlight_frame((left+right)//2, (top+bottom)//2, frame_width, frame_height, max(right-left, sf_width), max(bottom-top, sf_height))
            img = frame[sf_top:sf_bottom, sf_left:sf_right]
            # cv2.imshow("Without interpolation", img)
            img = cv2.resize(img, (640, 360), interpolation=cv2.INTER_AREA)
            # cv2.imshow("With interpolation", img)
            cv2.rectangle(frame,(sf_left,sf_top),(sf_right,sf_bottom),(0,255,0),2)
            # cv2.imshow('Processed image', super_resolution.upscale(img))
            # cv2.imshow('Raw Webcam', frame)
            # cv2.imshow('Webcam', frame)
            cam.send(img)
            cam.sleep_until_next_frame()

            key = cv2.waitKey(1)
            if key == 27:
                break

def spot_light_window(center_x, center_y, width, height):
    window_width, window_height = 640, 360
    top_left_x = center_x - (window_width//2)
    top_left_y = center_y - (window_height//2)

    bottom_right_x = center_x + (window_width//2)
    bottom_right_y = center_y + (window_height//2)

    if top_left_x < 0:
        top_left_x = 0
        bottom_right_x = 640

    if top_left_y < 0:
        top_left_y = 0
        bottom_right_y = 360

    if bottom_right_x > width:
        bottom_right_x = width
        top_left_x = width - 640

    if bottom_right_y > height:
        bottom_right_y = height
        top_left_y = height - 360

    return [top_left_x, top_left_y, bottom_right_x, bottom_right_y]

while True:
    status, frame = cap.read()
    width, height = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    n = len(faces)
    if len(faces) <= 1:
        x1, y1, x2, y2 = 0, 0, 0, 0
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
        x1, y1, x2, y2 = 0, 0, 0, 0
        for ele in face_cords:
            x1 += ele[0]
            y1 += ele[1]
            x2 += ele[2]
            y2 += ele[3]
         
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0, 255, 0), 2)
    
    # for face in faces:
    #     x1, y1 = face.left(), face.top()
    #     x2, y2 = face.right(), face.bottom()
        #cv2.rectangle(frame, (x1,y1), (x2,y2), (0, 255, 0), 1)
    z = 2*max(n,1)
    tlx, tly, brx, bry = spot_light_window((x1+x2)//z, (y1+y2)//z, 1280, 720)
    cv2.rectangle(frame,(tlx,tly),(brx,bry),(0,255,0),2)
    print(tlx, tly, brx, bry)

    #print(c1, c2, c3, c4)

    #print(width, height)
    # thresh = 180

    # crp_c0 = x1 - thresh if x1-thresh > 0 else thresh
    # crp_c1 = x2 + thresh if x2+thresh < width else width
    # crp_r0 = y1 - thresh if y1-thresh > 0 else thresh
    # crp_r1 = y2 + thresh if y2+thresh < height else height


    cv2.imshow('Spot-Light Footage-1', frame[tly+2:bry-2, tlx+2:brx-2])
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
