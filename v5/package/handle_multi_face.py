def handle_multi_face(faces, co_ords):
    face_co_ords = []
    x1, y1, x2, y2 = co_ords
    for face in faces:
        x1, y1 = face.left(), face.top()
        x2, y2 = face.right(), face.bottom()
        face_co_ords.append((x1, y1, x2, y2))
    x, y = 0, 0
    minx, maxy, maxx, miny = 10000, 0, 0, 10000
    for ele in face_co_ords:
        x += (ele[0]+ele[2])//2
        y += (ele[1]+ele[3])//2
        minx = min(minx, ele[0])
        maxy = max(maxy, ele[3])
        maxx = max(maxx, ele[2])
        miny = min(miny, ele[1])
    x, y = x//len(faces), y//len(faces)
    mul = 1
    while True:
        left = x-mul*16
        right = x+mul*16
        top = y-mul*9
        bottom = y+mul*9
        if left < minx and right > maxx and top < miny and bottom > maxy:
            x1, y1, x2, y2 = left, top, right, bottom
            break
        else:
            mul+=1
    return [x1, y1, x2, y2]