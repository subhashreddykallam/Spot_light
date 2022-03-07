def spotlight_frame(center_x, center_y, width, height, window_width, window_height):
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
