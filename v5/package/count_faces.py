def count_faces(faces):
    n = 0
    if faces.detections:
        for detection in faces.detections:
            n+=1
    return n