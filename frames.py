import numpy as np
import cv2
from cv2 import aruco
from augment import *
from markers import *

from color_detection import detect_color


def get_frames(cap, aruco_dict, parameters, detected, foods, timeout, updated, console):


    # capture frame by frame
    ret, frame = cap.read()
    # take the dimensions of the image
    frame_height, frame_width, frame_channels = frame.shape

    # covert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # detect the markers and frame them
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict,\
                                                      parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
    img1 = frame

    # keep a list of the variables and operators currently
    # in the frame
    curfood = []
    
    # we have detected at least one marker
    if (len(corners)):
        # create a 1D array of the markers 
        ids2 = ids.flatten()
        
        eindex = -1
        for id in ids2:
            # save the index in the corners array
            # that corresponds to the current id
            eindex += 1

            if (id == 1):
                if (not detected[id]):
                    food = Food(id, img1, eindex, frame, corners, frame_width, frame_height,\
                                console)
                    foods[id] = food
                curfood.append(foods[id])

        for food in curfood:
            eindex = -1

            for id in ids2:
                eindex += 1
                if (id == food.id):
                    food.update(eindex, img1, frame, corners)

            food.display()
            
            

    # we completed an operation so update the timeout counter
    if (updated):
        timeout += 1

    # if we reach timeout == 50, we can perform another operation
    if (timeout == 50):
        updated = False
    
    # if we quite
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return ()

    return [img1, frame_markers]
    


