def get_frame_center(frame_width, frame_height, sf_width, sf_height):
    return [(frame_width-sf_width)//2, (frame_height-sf_height)//2, sf_width+(frame_width-sf_width)//2, sf_height+(frame_height-sf_height)//2]
