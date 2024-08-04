import cv2
import numpy as np
import math

class CornerDetection:
    """
    A class to detect corners in an image.
    """

    def __init__(self):
        """
        Initialize the CornerDetection object.
        """
        pass

    def get_corner_detected(self, image):
        """
        Detect corners in the given image.

        Args:
            image (numpy.ndarray): The input image.

        Returns:
            bool: True if intersection detected, False otherwise.
        """
        h, w = image.shape[:2]
        blur = cv2.blur(image, (5, 5))
        ret, thresh1 = cv2.threshold(blur, 168, 255, cv2.THRESH_BINARY)
        hsv = cv2.cvtColor(thresh1, cv2.COLOR_RGB2HSV)
        lower_white = np.array([0, 0, 168])
        upper_white = np.array([172, 111, 255])
        mask = cv2.inRange(hsv, lower_white, upper_white)
        kernel_erode = np.ones((5, 5), np.uint8)
        eroded_mask = cv2.erode(mask, kernel_erode, iterations=1)
        kernel_dilate = np.ones((2, 2), np.uint8)
        dilated_mask = cv2.dilate(eroded_mask, kernel_dilate, iterations=2)

        contours, _ = cv2.findContours(dilated_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        black_background = np.zeros((h, w, 3), dtype=np.uint8)
        contour = cv2.drawContours(black_background, contours, -1, (255, 255, 255), 1)
        contour = cv2.dilate(contour, kernel_dilate, iterations=5)

        contour_open = self.apply_border_mask(contour, h, w)
        contour_gray = cv2.cvtColor(contour_open, cv2.COLOR_BGR2GRAY)
        lines = cv2.HoughLines(contour_gray, 1, np.pi / 180, 150, None, 0, 0)

        if lines is None:
            return False

        hough_angles = [line[0][1] for line in lines]
        return self.detect_intersection(hough_angles)

    def apply_border_mask(self, contour, h, w):
        """
        Apply border mask to the contour.

        Args:
            contour (numpy.ndarray): The contour image.
            h (int): Height of the image.
            w (int): Width of the image.

        Returns:
            numpy.ndarray: The masked contour image.
        """
        percentage = 0.07
        masks = [
            ((0, int(h * percentage)), (0, w)),
            ((-int(h * percentage), h), (0, w)),
            ((0, h), (0, int(w * percentage))),
            ((0, h), (-int(w * percentage), w))
        ]
        contour_open = contour.copy()
        for (y1, y2), (x1, x2) in masks:
            mask = np.ones_like(contour) * 255
            mask[y1:y2, x1:x2, :] = 0
            contour_open = cv2.bitwise_and(contour_open, mask)
        return contour_open

    def detect_intersection(self, hough_angles):
        """
        Detect intersection based on Hough angles.

        Args:
            hough_angles (list): List of angles from Hough transform.

        Returns:
            bool: True if intersection detected, False otherwise.
        """
        l = len(hough_angles)
        for i in range(l):
            for j in range(i, l):
                deviation = 0.03
                angle1 = hough_angles[i]
                angle2 = hough_angles[j]
                diff = abs(angle1 - angle2)
                if (1 - deviation) * math.pi / 2 <= diff <= (1 + deviation) * math.pi / 2:
                    return True
        return False
