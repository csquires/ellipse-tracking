import unittest
from math import tanh
import numpy as np
import cv2
import ellipse as e

class Ellipse_Test(unittest.TestCase):
	def setUp(self):
		center1 = (128,128)
		axes1 = (30,20)
		angle1 = 0
		self.ellipse1 = (center1,axes1,angle1)

		center2 = (126,124)
		axes2 = (22,31)
		angle2 = 1-90
		self.ellipse2 = (center2,axes2,angle2)

		center3 = (126,124)
		axes3 = (31,22)
		angle3 = 1-180
		self.ellipse3 = (center3,axes3,angle3)

	def test_standard_ellipse_orientation_no_change(self):
		actual_new_ellipse1 = e.standardize_ellipse(self.ellipse1)
		expected_new_ellipse1 = self.ellipse1
		self.assertEqual(expected_new_ellipse1, actual_new_ellipse1)

	def test_standard_ellipse_orientation_switch_axes(self):
		actual_new_ellipse2 = e.standardize_ellipse(self.ellipse2)
		expected_new_ellipse2 = ((126,124),(31,22),1)
		self.assertEqual(expected_new_ellipse2, actual_new_ellipse2)

	def test_standard_ellipse_orientation_negative_degrees(self):
		actual_new_ellipse3 = e.standardize_ellipse(self.ellipse3)
		expected_new_ellipse3 = ((126,124),(31,22),1)
		self.assertEqual(expected_new_ellipse3, actual_new_ellipse3)

	def test_ellipse_difference_no_difference(self):
		actual_ellipse_difference = e.ellipse_difference(self.ellipse2,self.ellipse3)
		expected_ellipse_difference = 0
		self.assertEqual(expected_ellipse_difference, actual_ellipse_difference)

	def test_closest_point_on_nice_ellipse_point_on_ellipse(self):
		axes = (50,40)
		pnt = (25,0)
		actual_closest_point = e.closest_point_on_nice_ellipse(pnt, axes)
		expected_closest_point = (25,0)
		self.assertEqual(expected_closest_point, actual_closest_point)

	def test_closest_point_on_ellipse_point_on_ellipse(self):
		pnt = (143,128)
		actual_closest_point = e.closest_point_on_ellipse(pnt, self.ellipse1)
		expected_closest_point = pnt
		# self.show_points_and_ellipse([pnt,actual_closest_point], self.ellipse1)
		self.assertEqual(expected_closest_point, actual_closest_point)

	def test_closest_point_on_ellipse_inside_ellipse_on_x0_axis(self):
		pnt = (141,128)
		actual_closest_point = e.closest_point_on_ellipse(pnt, self.ellipse1)
		expected_closest_point = (143,128)
		# self.show_points_and_ellipse([pnt,actual_closest_point], self.ellipse1)
		self.assertEqual(expected_closest_point, actual_closest_point)

	def test_closest_point_on_ellipse_outside_ellipse(self):
		pnt = (150,140)
		actual_closest_point = e.closest_point_on_ellipse(pnt, self.ellipse1)
		actual_closest_point = tuple(map(int, actual_closest_point))
		# self.show_points_and_ellipse([pnt,actual_closest_point], self.ellipse1)
		#TODO better check. currently validating by visual inspection

	def test_closest_point_on_ellipse_skewed_ellipse(self):
		ellipse = ((128,128),(90,40),45)
		pnt = (180,180)
		actual_closest_point = e.closest_point_on_ellipse(pnt, ellipse)
		actual_closest_point = tuple(map(int, actual_closest_point))
		self.show_points_and_ellipse(pnt,actual_closest_point, ellipse)
		#TODO better check. currently validating by visual inspection

	# for debugging purposes
	def show_ellipses(self):
		img = np.zeros((256,256,3), np.uint8)
		cv2.ellipse(img,self.ellipse1,(0,255,0))
		cv2.ellipse(img,self.ellipse2,(0,255,0))
		cv2.ellipse(img,self.ellipse3,(0,255,0))
		cv2.imshow("ellipses", img)
		cv2.waitKey(0)
	def show_points_and_ellipse(self,pnt,pnt_on_ellipse,ellipse):
		img = np.zeros((256,256,3), np.uint8)
		cv2.ellipse(img, ellipse, (0,255,0))
		cv2.circle(img, pnt, 2, (0,0,255))
		cv2.circle(img, pnt_on_ellipse, 2, (0,255,0))
		cv2.imshow("points and ellipse", img)
		cv2.waitKey(0)

if __name__ == '__main__':
	unittest.main()