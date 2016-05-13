import cv2
import fingertip_tracking as ft
import numpy as np

def record_video(output_filename):
	"""
	Records and displays video from your webcam, saving it in output_filename
	"""
	cap = cv2.VideoCapture(0)
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	out = cv2.VideoWriter(output_filename, fourcc, 20.0, (640,480))

	while cap.isOpened():
		ret, frame = cap.read()
		if ret == True:
			out.write(frame)
			cv2.imshow('frame', frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		else:
			break

	cap.release()
	out.release()
	cv2.destroyAllWindows()

def show_video_from_cap(cap):
	"""
	Shows a video from the cv2.VideoCapture object cap
	"""
	cap = cv2.VideoCapture(src)

	while cap.isOpened():
		ret, frame = cap.read()
		if ret == True:
			cv2.imshow('frame', frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		else:
			break

	cap.release()
	cv2.destroyAllWindows()

def show_img(img, window_name=""):
	"""
	Show image or images (via np.htack([img1,img2])) in window, close when q is presses
	"""
	cv2.imshow(window_name, img)
	while True:
		k = cv2.waitKey(0)
		if k & 0xFF == ord('q'):
			break
	cv2.destroyAllWindows()

def test_ellipse_detection(img):
	"""
	Testbed for ellipse detection code
	"""
	red_img = ft.get_red(img)
	show_img(red_img)

	ellipses = ft.get_ellipses_hsv(red_img,min_radius=10)
	ellipse_image = ft.get_ellipse_image(red_img, ellipses)
	show_img(ellipse_image)

# cap = cv2.VideoCapture('output.avi')
# show_video_from_cap(cap)
img = cv2.imread("img.jpg")