from scipy.optimize import bisect
from math import sqrt, log, cos, sin, radians
import numpy as np

def ellipse_difference(ellipse1,ellipse2,a=1,b=1,c=1):
	"""
	Error function from ellipse to ellipse

	Args:
		ellipse1: first ellipse to compare
		ellipse2: second ellipse to compare
		a: weight on displacement
		b: weight on log of area ratio
		c: weight of difference in angle
	Returns:
		'difference' between ellipses; weighted sum of displacement of centers, log of area ratio, and difference in angle
	"""
	#TODO: find better default parameters
	ellipse1 = standardize_ellipse(ellipse1)
	ellipse2 = standardize_ellipse(ellipse2)
	
	center1 = ellipse1[0]
	center2 = ellipse2[0]
	axes1 = ellipse1[1]
	axes2 = ellipse2[1]
	angle1 = ellipse1[2]
	angle2 = ellipse2[2]

	displacement = sqrt((center1[0]-center2[0])**2 + (center1[1]-center2[1])**2)
	size_change = log(axes1[0]*axes1[1]/(axes2[0]*axes2[1]))
	rotation = abs(angle1-angle2)

	return a*displacement + b*size_change + c*rotation

def standardize_ellipse(ellipse):
	"""
	Returns standardized ellipse: axes in order (large,small), and angle between 0 and 180

	Args:
		ellipse: ellipse to be put in standard form
	Returns:
		an equivalent ellipse with axes in order small,large and angle between 0 and 180
	"""
	center = ellipse[0]
	axes = ellipse[1]
	angle = ellipse[2]
	new_axes = tuple(sorted(axes, reverse=True))

	if new_axes != axes:
		angle += 90
	new_angle = angle % 180

	return (center,new_axes,new_angle)

def fit_error(ellipse,contour):
	"""
	Returns the difference between an ellipse and the set of contour points it should fit

	Args:
		ellipse: ellipse that fits contour
		contour: contour that ellipse was fitted to
	Returns:
		sum of distances of each point on contour to the ellipse
	"""
	error = 0.0
	for pnt in contour:
		pnt = tuple(pnt[0])
		error += distance_from_point_to_ellipse(pnt,ellipse)
	return error

def rotate(pnt, angle):
	"""
	Returns point rotated by angle

	Args:
		pnt: length-2 tuple of numbers
		angle: angle in degrees
	Returns:
		new length-2 tuple, equal to original point rotated counterclockwise by angle
	"""
	rad = radians(angle)
	x,y = pnt
	x_new = x*cos(rad) - y*sin(rad)
	y_new = y*cos(rad) + x*sin(rad)
	return (x_new,y_new)

def distance_from_point_to_ellipse(pnt,ellipse):
	"""
	Returns the distance from pnt to the closest point on ellipse

	Args:
		pnt: length-2 tuple of numbers
		ellipse: ellipses to compare point to
	Returns:
		distance from pnt to the closest point on ellipse
	"""
	assert type(pnt) == tuple

	x0, x1 = closest_point_on_ellipse(pnt, ellipse)
	y0, y1 = pnt

	return sqrt((x0-y0)**2 + ((x1-y1)**2))

def closest_point_on_ellipse(pnt,ellipse):
	"""
	Returns the closest point on ellipse to pnt

	Args:
		pnt: length-2 tuple of numbers
		ellipse: ellipses to compare point to
	Returns:
		closest point on ellipse to pnt
	"""
	assert type(pnt) == tuple

	ellipse = standardize_ellipse(ellipse)
	center = ellipse[0]
	axes = ellipse[1]
	angle = ellipse[2]

	#effectively center ellipse at zero and align it with axes by modifying point
	y0, y1 = pnt
	y0, y1 = (y0-center[0], y1-center[1])
	y0, y1 = rotate((y0,y1), angle)

	#make both coordinates of points positive
	flipped0 = flipped1 = False
	if y0 < 0:
		flipped0 = True
		y0 *= -1
	if y1 < 0:
		flipped1 = True
		y1 *= -1

	x0, x1 = closest_point_on_nice_ellipse((y0,y1), axes)

	#re-flip signs of point
	if flipped0:
		x0 *= -1
	if flipped1:
		x1 *= -1

	#re-rotate and uncenter resulting point
	x0,x1 = rotate((x0,x1), -angle)
	x0 = x0 + center[0]
	x1 = x1 + center[1]

	return (x0,x1)

def closest_point_on_nice_ellipse(pnt,axes):
	"""
	Returns the distance from a point in the first quadrant to an ellipse centered at the origin, aligned along axes

	Args:
		pnt: tuple (y0,y1), where y0,y1 >= 0
		ellipse: length of ellipse axes in decreasing order (axes[0] >= axes[1])
	Returns:
		distance from point to closest point on ellipse
	"""
	y0, y1 = pnt
	e0, e1 = map(lambda e: e/2., axes)
	assert e0 >= e1

	def distance_to_ellipse(t):
		return (e0*y0/(t+e0**2))**2 + (e1*y1/(t+e1**2))**2 - 1
	
	#find closest point given one of four cases
	#method from http://www.geometrictools.com/Documentation/DistancePointEllipseEllipsoid.pdf
	if y1 > 0:
		if y0 > 0:
			lower_bound = -e1**2 + e1*y1
			upper_bound = -e1**2 + sqrt(e0**2*y0**2 + e1**2*y1**2)
			tbar = bisect(distance_to_ellipse, lower_bound, upper_bound)
			x0 = e0**2*y0/(tbar+e0**2)
			x1 = e1**2*y1/(tbar+e1**2)
		else:
			x0 = 0
			x1 = e1
	else:
		if y0 < (e0**2 - e1**2)/e0:
			x0 = e0*2*y0/(e0**2-e1**2)
			x1 = e1*sqrt(1.-(x0/e0)**2)
		else:
			x0 = e0
			x1 = 0

	return (x0,x1)