import itertools
from math import tanh

def transition(original_map,new_objects,evaluation_function):
	"""
	Return map of new objects to ids given old objects and their ids that minimizes correspondence error

	Args:
		original_map: current map of objects to ids
		new_objects: new objects to be transitioned to
		evaluation_function: error function for objects
	Returns:
		new map of objects to ids
	"""
	original_objects = original_map.keys()
	o_length = len(original_objects)
	n_length = len(new_objects)

	best_correspondence = get_best_correspondence(original_objects,new_objects,evaluation_function)
	new_map = {}
	if len(original_map.values()) == 0 max_id = 0 else max_id = max(original_map.values())

	#assign objects corresponding ids or make new ids if there were more new objects than old
	for old_object,new_object in best_correspondence:
		if old_object in original_map:
			old_id = original_map[old_object]
			new_map[new_object] = old_id
		else:
			max_id += 1
			new_map[new_object] = max_id

	return new_map

def get_best_correspondence(list1,list2,evaluation_function):
	"""
	Get best correspondence between two lists (of possibly different size) given an evaluation function
	Args:
		list1: list of objects
		list2: list of same type of objects
		evaluation_function: function from a pair of objects to an error
	Returns:
		a list of pairings of objects or None that minimizes the evaluation function
	"""
	len_diff = len(list1) - len(list2)
	if len_diff > 0:
		list2.extend([None for i in range(len_diff)])
	elif len_diff < 0:
		list1.extend([None for i in range(-1*len_diff)])

	# TODO: make this multithreaded so that a timeout can be added
	possible_pairings = [zip(i,list2) for i in itertools.permutations(list1)]
	def f(pairing):
		return calculate_error(pairing,evaluation_function)
	best_correspondence = min(possible_pairings, key=f)

	return best_correspondence


def calculate_error(pairing,evaluation_function):
	"""
	Calculate the error of pairs of values given an error function
	Args:
		pairing: list of pairs of same type of object or None
		evaluation_function: function from a pair of objects to an error
	Returns:
		the total error of those pairings, which is the sum of the tanh of evaluation function
		if the pair is two objects and 1 if the pair includes a None
	"""
	def new_evaluation_function(object1,object2):
		if object1 is not None and object2 is not None:
			error = evaluation_function(object1,object2)
			#TODO: add scale so that largest error between objects is <1 (eg .75)
			return tanh(error) #sigmoid, between .5 and 1
		else:
			return 1

	return sum([new_evaluation_function(i,j) for i,j in pairing])