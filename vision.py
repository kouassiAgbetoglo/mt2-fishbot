import cv2 as cv
import numpy as np
from time import time
import math

class Vision:

    haystack_img_found = False
    fish_pos_x = None
    fish_pos_y = None
    fish_last_time = None

    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        if needle_img_path:
            self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)
            self.needle_w = self.needle_img.shape[1]
            self.needle_h = self.needle_img.shape[0]
        self.method = method

    def draw_game(self, haystack_img, roi=None):
        if roi is None:
            return
        else:
            line_color = (0, 255, 0)
            line_type = cv.LINE_4
            x, y, w, h = roi
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, 
                         lineType=line_type, thickness=2)
        return haystack_img
    
    @staticmethod
    def get_center(rectangles):
        if rectangles:
            x, y, w, h = rectangles[0]
            radius =  min(h, w) // 2
            center_x = x + int(h/2)
            center_y = y + int(w/2)
            return (center_x, center_y, radius)
        return 

    @staticmethod
    def circular_mask(haystack_img, center, radius):
        mask = np.zeros_like(haystack_img[:,:,0])
        cv.circle(mask, center, radius, 255, -1)
        masked_image = cv.bitwise_and(haystack_img, haystack_img, mask=mask)
        return masked_image

    def find(self, haystack_img, threshold=0.5, debug_mode=None, mask=None, info=False ):
        if mask is not None:
            masked_img = self.circular_mask(haystack_img, mask['center'], mask['radius'])
        else:
            masked_img = haystack_img

        result = cv.matchTemplate(masked_img, self.needle_img, self.method)
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        points = []
        if len(rectangles):
            
            if info:
                print('got image')

            line_color = (0, 255, 0)
            line_type = cv.LINE_4
            marker_color = (255, 0, 255)
            marker_type = cv.MARKER_CROSS

            for (x, y, w, h) in rectangles:
                center_x = x + int(w/2)
                center_y = y + int(h/2)
                points.append((x, y, h, w))
                if debug_mode == 'rectangles':
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)
                    cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, 
                                 lineType=line_type, thickness=2)
                elif debug_mode == 'points':
                    cv.drawMarker(haystack_img, (center_x, center_y), 
                                  color=marker_color, markerType=marker_type, 
                                  markerSize=40, thickness=2)
                elif debug_mode == 'circle':
                    radius =  min(h, w) // 2
                    cv.circle(haystack_img, (center_x, center_y), radius,
                              color=line_color, lineType=line_type, shift=0)

        if debug_mode:
            cv.imshow('Matches', haystack_img)
        
        return points

    def draw_rectangles(self, haystack_img, rectangles):
        # these colors are actually BGR
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        for (x, y, w, h) in rectangles:
            # determine the box positions
            top_left = (x, y)
            bottom_right = (x + h, y + w)
            # draw the box
            cv.rectangle(haystack_img, top_left, bottom_right, line_color, lineType=line_type)

        return haystack_img
    
    def draw_circle(self, haystack_img, circle, radius=None): # game circle
        line_color = (0, 255, 0)
        line_type = cv.LINE_4
        center_x, center_y, r = circle
        if not radius:
            radius = r
        cv.circle(haystack_img, (center_x, center_y+2), radius,
                              color=line_color, lineType=line_type, shift=0)
        return haystack_img

    def detect(self, haystack_img):

        # match the needle_image with the hasytack image
        result = cv.matchTemplate(haystack_img, self.needle_img, cv.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        # needle_image's dimensions
        needle_w = self.needle_img.shape[1]
        needle_h = self.needle_img.shape[0]

        # get the position of the match image
        top_left = max_loc
        bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

        

        # Only the max level of match is greater than 0.5
        if max_val > 0.5:
            pos_x = (top_left[0] + bottom_right[0])/2
            pos_y = (top_left[1] + bottom_right[1])/2

            if self.fish_last_time:
                dist = math.sqrt((pos_x - self.fish_pos_x)**2 + (self.fish_pos_y - pos_y)**2)
                cv.rectangle(haystack_img, top_left, bottom_right,
                            color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

                # Calculate the fish velocity
                velo = dist/(time() - self.fish_last_time)

                if velo == 0.0:
                    return (pos_x, pos_y, True)
                elif velo >= 150:

                    # With this velocity the fish position will be predict

                    pro = 30 / dist
                    destiny_x = int(pos_x + (pos_x - self.fish_pos_x) * pro)
                    destiny_y = int(pos_y + (pos_y - self.fish_pos_y) * pro)

                    # Draw the predict line

                    cv.line(haystack_img, (int(pos_x), int(pos_y)),
                            (destiny_x, destiny_y), (0, 255, 0),  thickness=3)
                    
                    cv.imshow(' z', haystack_img)

                    return (destiny_x, destiny_y, False)

            # get the fish position and the time

            self.fish_pos_x = pos_x
            self.fish_pos_y = pos_y
            self.fish_last_time = time()

        return None