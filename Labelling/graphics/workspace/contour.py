from typing import List

import cv2
import numpy as np
from PIL import Image


################################################################################
# Code courtesy of @uppala75 at
# https://github.com/uppala75/CarND-Advanced-Lane-Lines

# Define a function that takes an image, gradient orientation,
# and threshold min / max values.

def abs_sobel_thresh(img, orient='x', thresh_min=25, thresh_max=255):
    # Convert to grayscale
    # gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS).astype(np.float)
    l_channel = hls[:,:,1]
    s_channel = hls[:,:,2]
    # Apply x or y gradient with the OpenCV Sobel() function
    # and take the absolute value
    if orient == 'x':
        abs_sobel = np.absolute(cv2.Sobel(l_channel, cv2.CV_64F, 1, 0))
    if orient == 'y':
        abs_sobel = np.absolute(cv2.Sobel(l_channel, cv2.CV_64F, 0, 1))
    # Rescale back to 8 bit integer
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
    # Create a copy and apply the threshold
    binary_output = np.zeros_like(scaled_sobel)
    # Here I'm using inclusive (>=, <=) thresholds, but exclusive is ok too
    binary_output[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1

    # Return the result
    return binary_output


# Define a function to return the magnitude of the gradient for a given sobel
# kernel size and threshold values
def mag_thresh(img, sobel_kernel=3, mag_thresh=(0, 255)):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Take both Sobel x and y gradients
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    # Calculate the gradient magnitude
    gradmag = np.sqrt(sobelx**2 + sobely**2)
    # Rescale to 8 bit
    scale_factor = np.max(gradmag)/255
    gradmag = (gradmag/scale_factor).astype(np.uint8)
    # Create a binary image of ones where threshold is met, zeros otherwise
    binary_output = np.zeros_like(gradmag)
    binary_output[(gradmag >= mag_thresh[0]) & (gradmag <= mag_thresh[1])] = 1

    # Return the binary image
    return binary_output


# Define a function to threshold an image for a given range and Sobel kernel
def dir_threshold(img, sobel_kernel=3, thresh=(0, np.pi/2)):
    # Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Calculate the x and y gradients
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    # Take the absolute value of the gradient direction,
    # apply a threshold, and create a binary image result
    absgraddir = np.arctan2(np.absolute(sobely), np.absolute(sobelx))
    binary_output =  np.zeros_like(absgraddir)
    binary_output[(absgraddir >= thresh[0]) & (absgraddir <= thresh[1])] = 1

    # Return the binary image
    return binary_output


def color_threshold(image, sthresh=(0,255), vthresh=(0,255)):
    hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
    s_channel = hls[:,:,2]
    s_binary = np.zeros_like(s_channel)
    s_binary[(s_channel > sthresh[0]) & (s_channel <= sthresh[1])] = 1

    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    v_channel = hsv[:,:,2]
    v_binary = np.zeros_like(v_channel)
    v_binary[(v_channel > vthresh[0]) & (v_channel <= vthresh[1])] = 1

    output = np.zeros_like(s_channel)
    output[(s_binary == 1) & (v_binary) == 1] = 1

    # Return the combined s_channel & v_channel binary image
    return output


def s_channel_threshold(image, sthresh=(0,255)):
    hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
    s_channel = hls[:, :, 2]  # use S channel

    # create a copy and apply the threshold
    binary_output = np.zeros_like(s_channel)
    binary_output[(s_channel >= sthresh[0]) & (s_channel <= sthresh[1])] = 1
    return binary_output


def window_mask(width, height, img_ref, center, level):
    output = np.zeros_like(img_ref)
    output[int(img_ref.shape[0]-(level+1)*height):int(img_ref.shape[0]-level*height), max(0,int(center-width)):min(int(center+width),img_ref.shape[1])] = 1
    return output

################################################################################


def _get_contours(cv_image: np.ndarray, threshold: int) -> List[np.ndarray]:
    img_grey = cv2.cvtColor(np.array(cv_image), cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(img_grey, threshold, 255, 0)
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    return contours


def _test_this_out(undistTest):
    # Apply Sobel operator in X-direction to experiment with gradient thresholds
    gradx = abs_sobel_thresh(
        undistTest, orient='x', thresh_min=20, thresh_max=100
    )
    grady = abs_sobel_thresh(undistTest, orient='y', thresh_min=25, thresh_max=255)
    # Apply magnitude threshold
    magThr = mag_thresh(undistTest, sobel_kernel=3, mag_thresh=(30, 100))
    dirThr = dir_threshold(undistTest, sobel_kernel=31, thresh=(0.5, 1))
    # use s channel alone in HLS colorspace and experiment with thresholds
    s_binary = s_channel_threshold(undistTest, sthresh=(170, 255))
    # Experiment with HLS & HSV color spaces along with thresholds
    c_binary = color_threshold(
        undistTest, sthresh=(100, 255), vthresh=(50, 255)
    )
    # Combine the binary images using the Sobel thresholds in X/Y directions along with the color threshold to form the final image pipeline
    preprocessImage = np.zeros_like(undistTest[:, :, 0])
    preprocessImage[((gradx == 1) & (grady == 1) | (c_binary == 1))] = 255
    cv2.imshow("undistTest", undistTest)
    cv2.imshow("gradx", gradx)
    cv2.imshow("grady", grady)
    cv2.imshow("magThr", magThr)
    cv2.imshow("dirThr", dirThr)
    cv2.imshow("s_binary", s_binary)
    cv2.imshow("c_binary", c_binary)
    cv2.imshow("preprocessImage", preprocessImage)


def _test_this_out_too(img):
    preprocessImage = np.zeros_like(img[:, :, 0])
    gradx = abs_sobel_thresh(img, orient='x', thresh_min=12, thresh_max=255)
    grady = abs_sobel_thresh(img, orient='y', thresh_min=25, thresh_max=255)
    c_binary = color_threshold(img, sthresh=(100, 255), vthresh=(50, 255))
    preprocessImage[((gradx == 1) & (grady == 1) | (c_binary == 1))] = 255
    cv2.imshow("gradx", gradx)
    cv2.imshow("grady", grady)
    cv2.imshow("c_binary", c_binary)
    cv2.imshow("preprocessImage", preprocessImage)


def get_contours(x: int, y: int, pil_image: Image):
    pil_rgb_img = pil_image.convert("RGB")
    img = cv2.cvtColor(np.array(pil_rgb_img), cv2.COLOR_RGB2BGR)

    # _test_this_out(img)
    # _test_this_out_too(img)

    contours = _get_contours(img, threshold=127)
    # cv2.drawContours(img, contours, -1, (0, 255, 0), 1)

    contours = _get_contours(img, threshold=100)
    # cv2.drawContours(img, contours, -1, (0, 0, 255), 1)

    contours = _get_contours(img, threshold=95)
    # cv2.drawContours(img, contours, -1, (255, 0, 0), 1)
    # Get contours surrounding the point. Code courtesy of @Jeru-Luke and
    # @JoSSte StackOverflow
    # https://stackoverflow.com/questions/50670326/how-to-check-if-point-is-placed-inside-contour
    # The check that it is non-negative means that the point either falls on
    # the line of the contour or inside the contour.
    contours = [c for c in contours if cv2.pointPolygonTest(c, (x, y), True) >= 0]
    contours = list(sorted(contours, key=lambda a: cv2.contourArea(a)))
    # cv2.drawContours(img, contours, -1, (255, 0, 0), 3)
    # cv2.imshow("Contours", img)

    return contours


