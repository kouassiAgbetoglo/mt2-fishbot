import cv2 as cv
import numpy as np

class Vision:
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

    def find(self, haystack_img, threshold=0.5, debug_mode=None, mask=None):
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
