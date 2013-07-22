from collections import OrderedDict


from .common import Generator

class Linear(Generator):
	out_type = "SCALAR"

	type_map =	OrderedDict((
					("slope", "SCALAR"),
					("intercept", "SCALAR"),
				))

	__slots__ = type_map.keys()

	def __init__(self, slope=0.05, intercept=0.0):
		self.slope = slope
		self.intercept = intercept

	def get_value(self, x):
		return self.slope * x + self.intercept