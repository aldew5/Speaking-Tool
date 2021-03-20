import numpy as np
import cv2

#image = cv2.imread("_data/blue_marker.jpg")

def detect_color(image, color):


    # convert image from BGR to HSV (hue-saturation value)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # set ranges for red
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsv_image, red_lower, red_upper)

    # green
    green_lower = np.array([25, 52, 72], np.uint8)
    green_upper = np.array([102, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsv_image, green_lower, green_upper)

    # blue
    blue_lower = np.array([94, 80, 2], np.uint8) 
    blue_upper = np.array([120, 255, 255], np.uint8) 
    blue_mask = cv2.inRange(hsv_image, blue_lower, blue_upper) 

    # Morphological transform, dilatio n for each color and bitwise_and
    # operator between image and mask detects only a particular color

    kernal = np.ones((5, 5), "uint8")

    if (color == "red"):
        red_mask = cv2.dilate(red_mask, kernal)
        res_red = cv2.bitwise_and(image, image, mask=red_mask)

        # Creating contour to track red color 
        contours, hierarchy = cv2.findContours(red_mask, 
                                               cv2.RETR_TREE, 
                                               cv2.CHAIN_APPROX_SIMPLE) 
          
        for pic, contour in enumerate(contours): 
            area = cv2.contourArea(contour) 
            if(area > 300):

                # redundant code for display (not used here)
                x, y, w, h = cv2.boundingRect(contour) 
                imageFrame = cv2.rectangle(image, (x, y),  
                                           (x + w, y + h),  
                                           (0, 0, 255), 2) 
                  
                cv2.putText(image, "Red Colour", (x, y), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                            (0, 0, 255))
                return True


    elif (color == "green"):
        green_mask = cv2.dilate(green_mask, kernal)
        res_green = cv2.bitwise_and(image, image, mask=green_mask)

        contours, hierarchy = cv2.findContours(green_mask, 
                                               cv2.RETR_TREE, 
                                               cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                # redundant code for display (not used here)
                x, y, w, h = cv2.boundingRect(contour) 
                imageFrame = cv2.rectangle(image, (x, y),  
                                           (x + w, y + h),  
                                           (0, 0, 255), 2) 
                  
                cv2.putText(image, "Green Colour", (x, y), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                            (0, 255, 0))
                return True

    elif (color == "blue"):
        blue_mask = cv2.dilate(blue_mask, kernal) 
        res_blue = cv2.bitwise_and(image, image, 
                               mask=blue_mask)
        contours, hierarchy = cv2.findContours(blue_mask, 
                                               cv2.RETR_TREE, 
                                               cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            
            if (area > 300):
                # redundant code for display (not used here)
                x, y, w, h = cv2.boundingRect(contour) 
                imageFrame = cv2.rectangle(image, (x, y),  
                                           (x + w, y + h),  
                                           (0, 0, 255), 2) 
                  
                cv2.putText(image, "Blue Colour", (x, y), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                            (255, 0, 0))

                return True
                
          
        #cv2.imshow("HIGH", image)
    else:
        print("Invalid color")
    
    return False
    

