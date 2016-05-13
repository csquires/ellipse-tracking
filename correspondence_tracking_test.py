import unittest
from math import tanh
import correspondence_tracking

class ComplexNum:
	def __init__(self,a,b):
		self.a = a
		self.b = b
	def error(self,other):
		return abs(self.a-other.a) + abs(self.b-other.b)
	def __str__(self):
		return str(self.a) + " + " + str(self.b) + "i"
	def __eq__(self,other):
		if not isinstance(other, ComplexNum):
			return False 
		return self.a == other.a and self.b == other.b
	def __hash__(self):
		return hash(self.a) + hash(self.b)

class Correspondence_Tracking_Test(unittest.TestCase):
	def setUp(self):
		self.original_dict = {}
		self.original_dict[ComplexNum(1,2)] = 1
		self.original_dict[ComplexNum(1,3)] = 2

		self.new_objects = [ComplexNum(1,2),ComplexNum(1,3.1),ComplexNum(2,4)]

	def test_transition(self):
		actual_new_dict = correspondence_tracking.transition(self.original_dict,self.new_objects,ComplexNum.error)
		
		expected_new_dict = {}
		expected_new_dict[ComplexNum(1,2)] = 1
		expected_new_dict[ComplexNum(1,3.1)] = 2
		expected_new_dict[ComplexNum(2,4)] = 3

		self.assertEqual(actual_new_dict, expected_new_dict)

	def test_get_best_correspondence(self):
		original_objects = self.original_dict.keys()
		original_objects.append(None)
		actual_pairs = correspondence_tracking.get_best_correspondence(original_objects,self.new_objects,ComplexNum.error)
		expected_pairs = []
		expected_pairs.append((ComplexNum(1,2),ComplexNum(1,2)))
		expected_pairs.append((ComplexNum(1,3),ComplexNum(1,3.1)))
		expected_pairs.append((None,ComplexNum(2,4)))
		
		self.assertEqual(sorted(expected_pairs), sorted(actual_pairs))

	def test_calculate_error_multiple_items(self):
		original_objects = self.original_dict.keys()
		original_objects.append(None)
		pairs = zip(original_objects,self.new_objects)
		actual_error = correspondence_tracking.calculate_error(pairs,ComplexNum.error)
		error0 = 0
		error1 = tanh(ComplexNum(1,3).error(ComplexNum(1,3.1)))
		error2 = 1
		expected_error = error0 + error1 + error2
		self.assertEqual(expected_error, actual_error)

	def test_calculate_error_no_error(self):
		pairs = [(ComplexNum(1, 2),ComplexNum(1, 2))]
		actual_error = correspondence_tracking.calculate_error(pairs,ComplexNum.error)
		self.assertEqual(0, actual_error)

	def test_calculate_error_object_is_none(self):
		pairs = [(None,ComplexNum(2, 4))]
		actual_error = correspondence_tracking.calculate_error(pairs,ComplexNum.error)
		self.assertEqual(1, actual_error)

	# for debugging
	def print_pairs(self,pairs):
		for original, new in pairs:
			print "original: ", original, "; new: ", new

if __name__ == '__main__':
	unittest.main()