import cv2
import math
import numpy as np
from skimage.morphology import skeletonize
from skimage import img_as_ubyte

def detect_v3(image):
    """
    Detect intersection in the given image.

    Args:
        image (numpy.ndarray): The input image.

    Returns:
        tuple: A tuple containing:
            - blackcanvas (numpy.ndarray): Image with Hough lines drawn.
            - end (bool): True if intersection detected, False otherwise.
    """
    h, w = image.shape[:2]
    blur = cv2.blur(image, (5, 5))
    ret, thresh1 = cv2.threshold(blur, 168, 255, cv2.THRESH_BINARY)
    hsv = cv2.cvtColor(thresh1, cv2.COLOR_RGB2HSV)
    lower_white = np.array([0, 0, 168])
    upper_white = np.array([172, 111, 255])
    mask = cv2.inRange(hsv, lower_white, upper_white)
    kernel_erode = np.ones((6, 6), np.uint8)
    eroded_mask = cv2.erode(mask, kernel_erode, iterations=1)
    kernel_dilate = np.ones((4, 4), np.uint8)
    dilated_mask = cv2.dilate(eroded_mask, kernel_dilate, iterations=1)
    contours, _ = cv2.findContours(dilated_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    black_background = np.zeros((h, w, 3), dtype=np.uint8)
    contour = cv2.drawContours(black_background, contours, -1, (255, 255, 255), 1)
    contour_gray = cv2.cvtColor(contour, cv2.COLOR_BGR2GRAY)
    erosion = cv2.erode(contour_gray, np.ones((20, 20), np.uint8), iterations=1)
    lines = cv2.HoughLines(contour_gray, 1, np.pi / 180, 150, None, 0, 0)
    blackcanvas = np.zeros_like(contour)

    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
            cv2.line(blackcanvas, pt1, pt2, (0, 0, 255), 1, cv2.LINE_AA)

    hough_angles = [line[0][1] for line in lines] if lines is not None else []
    return blackcanvas, detect_intersection(hough_angles)

def detect_intersection(hough_angles):
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
            deviation = 0.1
            angle1 = hough_angles[i]
            angle2 = hough_angles[j]
            diff = abs(angle1 - angle2)
            if (1 - deviation) * math.pi / 2 <= diff <= (1 + deviation) * math.pi / 2:
                return True
    return False
