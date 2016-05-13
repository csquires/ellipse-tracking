# ellipse-tracking

Set of modules for basic image processing, operations on ellipses, and tracking of objects over time.

Required libraries: scipy, numpy

Modules:
  - ellipse: functions to determine 'difference' between two ellipses, to format ellipse in standard format, and to find
    the closest point on the ellipse to some other point/distance between those points.
  - correspondence tracking: functions to get best correspondence between two lists given a way to evaluate the difference
    between their objects, and to transition from one map of objects to ids to another, matching ids to matching objects
  - fingertip_tracking: functions to change rgb images to hsv, functions to get contours or ellipses in hsv or binary images,
    methods to get images with contours or ellipses drawn on, and a function to follow ellipses through a video

Contact: csquires@mit.edu
