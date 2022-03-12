import cv2

def handle_single_face(faces, co_ords):
    x1, y1, x2, y2 = co_ords
    for face in faces:
        x1, y1 = face.left(), face.top()
        x2, y2 = face.right(), face.bottom()
    return [x1, y1, x2, y2]
