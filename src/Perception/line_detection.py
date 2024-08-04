import cv2
import numpy as np

class LineDetection:
    """
    A class to detect lines in an image.
    """

    def __init__(self):
        """
        Initialize the LineDetection object.
        """
        pass

    def get_line_detected(self, image):
        """
        Detect the line in the given image.

        Args:
            image (numpy.ndarray): The input image.

        Returns:
            list: Coordinates of the detected line's centroid relative to image center.
        """
        h, w = image.shape[:2]
        blur = cv2.blur(image, (20, 20))
        ret, thresh1 = cv2.threshold(blur, 168, 255, cv2.THRESH_BINARY)
        hsv = cv2.cvtColor(thresh1, cv2.COLOR_RGB2HSV)
        lower_white = np.array([0, 0, 168])
        upper_white = np.array([172, 111, 255])
        mask = cv2.inRange(hsv, lower_white, upper_white)
        kernel_erode = np.ones((10, 6), np.uint8)
        eroded_mask = cv2.erode(mask, kernel_erode, iterations=4)
        kernel_dilate = np.ones((5, 2), np.uint8)
        dilated_mask = cv2.dilate(eroded_mask, kernel_dilate, iterations=2)
        contours, _ = cv2.findContours(dilated_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

        if contours:
            M = cv2.moments(contours[0])
            try:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                return [cx - w / 2, h - cy]
            except ZeroDivisionError:
                return [0, 10]
        return [0, 10]
