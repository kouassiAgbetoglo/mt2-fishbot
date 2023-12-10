import cv2 as cv
import numpy as np


class Vision:

    # properties
    needle_img = None
    needle_w = 0
    needle_h = 0
    method = None

    # constructor
    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)

        # Save the dimensions of the needle image
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]
        # There are 6 methods to choose from:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method

    def draw_game(self, haystack_img, roi = None):
        if roi is None:
                return
        else:
            line_color = (0, 255, 0)
            line_type = cv.LINE_4
            x, y, w, h = roi
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # Draw the box
            cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, 
                                lineType=line_type, thickness=2)


    def find(self, haystack_img, threshold=0.5, debug_mode=None, roi = None):

        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)

        # Get the all the positions from the match result that exceed our threshold
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

            line_color = (0, 255, 0)
            line_type = cv.LINE_4
            marker_color = (255, 0, 255)
            marker_type = cv.MARKER_CROSS

            # Loop over all the rectangles
            for (x, y, w, h) in rectangles:

                # Determine the center position
                center_x = x + int(w/2)
                center_y = y + int(h/2)
                # Save the points
                points.append((x, y, h, w))

                if debug_mode == 'rectangles':
                    # Determine the box position
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)
                    # Draw the box
                    cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, 
                                lineType=line_type, thickness=2)
                elif debug_mode == 'points':
                    # Draw the center point
                    cv.drawMarker(haystack_img, (center_x, center_y), 
                                color=marker_color, markerType=marker_type, 
                                markerSize=40, thickness=2)
                elif debug_mode == 'circle':
                    pass

        if debug_mode:
            cv.imshow('Matches', haystack_img)
        
        return points

        
    
    def cropCircle(self, image):
        im1 = cv.imread(image, cv.IMREAD_UNCHANGED)
        h, w = im1.shape[:2]
        circularMask = np.zeros((h, w), np.uint8)
        th = -8
        center = (w // 2, (h // 2) - th) 
        radius = min(h, w)  // 4
        cv.circle(circularMask, center, radius, (255, 255, 255), -1, cv.LINE_AA)
        cropedIm1 = cv.bitwise_and(im1, im1, mask=circularMask)
        return cropedIm1