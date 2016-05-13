import cv2
import numpy as np
import correspondence_tracking as ct
from ellipse import *

"""
IMPORTANT NOTE:
this class makes defensive copies of images whenever using methods that modify
the original image (e.g. drawContours, drawEllipses). This allows a functional
programming style to be applied, without concern of the original object mutating.
However, this incurs a performance penalty due to copying, so if this becomes an
issue it may be necessary to port all methods that use the copy() function to
mutable versions.
"""

# -----------------------------------------------------------
# rrb -> hsv image methods
# -----------------------------------------------------------
def hsv_mask(hsv_img,lower,upper):
	"""
	Returns the part of the image with hue between lower and upper

	Args:
		hsv_img: image to extract hue range from
		lower: lower bound on hue
		upper: upper bound on hue
	Returns:
		image with parts outside of range lower to upper blacked out
	"""
	lower_hsv = np.array([lower,50,50])
	upper_hsv = np.array([upper,255,255])
	return cv2.inRange(hsv_img, lower_hsv, upper_hsv)

def get_red(img, lower_red_bounds=(0,2), upper_red_bounds=(170,180)):
	"""
	Returns the part of the image that is red

	Args:
		img: image to extract red from
	Returns:
		hsv version of image with non-red parts blacked out
	"""
	img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	lower_red0, upper_red0 = lower_red_bounds
	mask0 = hsv_mask(img_hsv, lower_red0, upper_red0)

	lower_red1, upper_red1 = upper_red_bounds
	mask1 = hsv_mask(img_hsv, lower_red1, upper_red1)

	mask = mask0 + mask1
	img_red = cv2.bitwise_and(img, img, mask=mask)

	return img_red

# -----------------------------------------------------------
# hsv image methods
# -----------------------------------------------------------
def get_thresholded_hsv(hsv_img):
	"""
	Returns binary copy of hsv_img using optimal threshold (via Otsu method)

	Args:
		hsv_img: image to apply thresholding to
	Returns:
		copy of hsv_img with white in place of pixels with gray value over optimal threshold and black in place of pixels below
	"""
	gray = hsv_img[:,:,2]
	maxval = 255 #black
	ret, thresh = cv2.threshold(gray, 0, maxval, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	return thresh

def get_contours_hsv(hsv_img,fill=True):
	"""
	Returns list of contours from an hsv image

	Args:
		hsv_img: an image in hsv format
		fill: whether or not to first apply dilation and erosion before getting contours
	Returns:
		list of contours found in image (via simple chain approximation)
	"""
	binary_img = get_thresholded_hsv(hsv_img)
	if fill:
		binary_img = get_filled_binary(binary_img)
	return get_contours_binary(binary_img)

def get_ellipses_hsv(hsv_img,min_radius=0,fill=True):
	"""
	Returns list of ellipses in an hsv img

	Args:
		hsv_img: image to find ellipses on
		min_radius: minimum radius of ellipse to consider
		fill: whether or not to first apply dilation and erosion before getting contours
	Returns:
		list of ellipses found in the image
	"""
	contours = get_contours_hsv(hsv_img,fill)

	#need more than 4 points to fit ellipse
	contours = filter(lambda c: len(c) > 4, contours)

	#pair ellipses with their contours for next steps
	ellipses_contour_pairs = zip(map(cv2.fitEllipse, contours),contours)

	#filter out small ellipses
	ellipses_contour_pairs = filter(lambda (e,c): min(e[1]) > min_radius, ellipses_contour_pairs)

	#get top 5 ellipses
	ellipses_contour_pairs = sorted(ellipses_contour_pairs, key= lambda (e,c): fit_error(e,c))[:5]

	#extract ellipses from pairs
	ellipses = map(lambda (e,c): e, ellipses_contour_pairs)

	return ellipses

# -----------------------------------------------------------
# binary image methods
# -----------------------------------------------------------
def get_contours_binary(binary_img):
	"""
	Returns list of contours from a binary image

	Args:
		binary_img: an image with only black and white pixels
	Returns:
		list of contours found in image (via simple chain approximation)
	"""
	im2, contours, hierarchy = cv2.findContours(binary_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	return contours

def get_ellipses_binary(binary_img,min_radius=0):
	"""
	Returns list of ellipses in a binary img

	Args:
		binary_img: image to find ellipses on
		min_radius: minimum radius of ellipse to consider
	Returns:
		list of ellipses found in the image
	"""
	contours = get_contours_binary(binary_img)

	#need more than 4 points to fit ellipse
	contours = filter(lambda c: len(c) > 4, contours)

	#pair ellipses with their contours for next steps
	ellipses_contour_pairs = zip(map(cv2.fitEllipse, contours),contours)

	#filter out small ellipses
	ellipses_contour_pairs = filter(lambda (e,c): min(e[1]) > min_radius, ellipses_contour_pairs)

	#get top 5 ellipses
	ellipses_contour_pairs = sorted(ellipses_contour_pairs, key= lambda (e,c): -1*fit_error(e,c))[:5]

	#extract ellipses from pairs
	ellipses = map(lambda (e,c): e, ellipses_contour_pairs)

	return ellipses

def get_filled_binary(binary_img, kernel_size=3, iterations=3):
	"""
	Returns the image with opening and closing operations applied on it

	Args:
		binary_img: and= image with only black and white pixels
		kernel_size: size of kernel used for opening and closing, must be odd
		iterations: number of times opening and closing are applied
	Returns:
		the image after opening and closing are applied
	"""
	kernel = np.ones((kernel_size,kernel_size),np.uint8)

	opened_img = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel, iterations=iterations)
	dilated_img = cv2.dilate(opened_img, kernel, iterations=iterations)

	return dilated_img

# -----------------------------------------------------------
# drawing methods
# -----------------------------------------------------------
def get_contour_image(img,contours):
	"""
	Returns copy of image with contours overlaid

	Args:
		img: image to overlay contours on
		contours: list of contours to overlay on image
	Returns:
		copy of image with contours overlaid
	"""
	img_copy = img.copy()
	cv2.drawContours(img_copy, contours, -1, (0,255,0))
	return img_copy

def get_ellipse_image(img,ellipses):
	"""
	Returns copy of img with ellipses overlaid

	Args:
		img: img to overlay ellipses on
		ellipses: ellipses to be overlaid on image
	Returns:
		copy of image with ellipses overlaid
	"""
	img_copy = img.copy()
	for ellipse in ellipses:
		cv2.ellipse(img_copy, ellipse, (0,255,0))
	return img_copy

# -----------------------------------------------------------
# main algorithm for fingertip tracking
# -----------------------------------------------------------
def follow_ellipses(cap,draw_contours=False,draw_ellipses=False):
	"""
	Tracking algorithm to follow red ellipses throughout video

	Args:
		cap: cv2.VideoCapture object
		draw_contours: whether or not to draw the contours on each frame
		draw_ellipses: whether or not to draw the ellipses on each frame
	Returns:
		list of dictionaries that map ellipses to ids
	"""
	current_ellipses = None
	dictionaries = []

	while cap.isOpened():
		previous_ellipses = current_ellipses
		
		ret, frame = cap.read()
		if ret != True: break
		red_img = get_red(frame)
		images = [red_img]

		if draw_contours:
			contours = get_contours_hsv(red_img)
			contour_image = get_contours_hsv(red_img, contours)
			images.append(contour_image)
		if draw_ellipses:
			current_ellipses = get_ellipses_hsv(red_img)
			ellipse_image = get_ellipse_image(red_img, ellipses)
			images.append(ellipse_image)
		cv2.imshow("red circles", np.hstack(images))

		#special behavior on first frame
		if previous_ellipses is None:
			current_dict = {}
			counter = 0
			if current_ellipses is not None:
				for ellipse in current_ellipses:
					current_dict[ellipse] = counter
					counter += 1
		else:
			dictionaries.append(current_dict)
			current_dict = ct.transition(current_dict,current_ellipses,ellipse_difference)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cap.release()
	return dictionaries