import numpy as np
import cv2
from cv2 import aruco
from augment import *
import time


class Marker(object):
    """
    An abstract class that defines some methods all markers in the program
    will use
    """
    def __init__(self, id, eindex, image, frame, corners, frame_width, frame_height, console):
        self.id = id
        self.eindex = eindex
        self.frame = frame
        self.image = image
        self.corners = corners
        self.width, self.height = 200, 200
        self.frame_width, self.frame_height = frame_width, frame_height
        self.console = console
        
    # must be updated for each new frame
    def update(self, eindex, image, frame, corners):
        self.eindex = eindex
        self.image = image
        self.frame = frame
        self.corners = corners  
        
    # augments the ArUco Marker
    def display(self, video_frame, image):
        augment(self.eindex, self.frame, self.corners, (self.width, self.height), video_frame,\
                (self.frame_width, self.frame_height), image)


class Food(Marker):

    def __init__(self, id, image, eindex, frame, corners, frame_width, frame_height, console):
        Marker.__init__(self, id, eindex, image, frame, corners, frame_width, frame_height, console)

        # display a menu to choose food options in the console
        self.type = console.get_input("Pick a type of food (pizza or hotdog): ")
        time.sleep(1)

    def display(self):
        if self.type == "pizza":
            pizza = cv2.imread("_data/pizza.jpeg")
            Marker.display(self, pizza, self.image)
        elif self.type == "hotdog":
            hotdog = cv2.imread("_data/hotdog.jpeg")
            Marker.display(self, hotdog, self.image)
