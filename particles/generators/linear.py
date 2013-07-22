from collections import OrderedDict


from .common import Generator

class Linear(Generator):
	out_type = "SCALAR"

	type_map =	OrderedDict((
					("slope", "SCALAR"),
					("intercept", "SCALAR"),
				))

	__slots__ = type_map.keys()

	def __init__(self, m=0.05, b=0.0):
		self.slope = m
		self.intercept = b

	def get_value(self, x):
		return self.slope * x + self.intercept