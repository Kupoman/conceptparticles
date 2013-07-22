from collections import OrderedDict
from .common import Generator

class Mix3(Generator):
	out_type = "VECTOR"

	type_map =	OrderedDict((
					("x_generator", "GENERATOR_SCALAR"),
					("y_generator", "GENERATOR_SCALAR"),
					("z_generator", "GENERATOR_SCALAR"),
				))

	__slots__ = type_map.keys()

	def __init__(self, factory, n1="", d1={}, n2="", d2={}, n3="", d3={}):
		self.x_generator = self.y_generator = self.z_generator = None

		if n1:
			self.x_generator = factory(n1, d1)
		if n2:
			self.y_generator = factory(n2, d2)
		if n3:
			self.z_generator = factory(n3, d3)

	def get_value(self, x):
		value = [0, 0, 0]
		if self.x_generator:
			value[0] = self.x_generator.get_value(x)
		if self.y_generator:
			value[1] = self.y_generator.get_value(x)
		if self.z_generator:
			value[2] = self.z_generator.get_value(x)

		return value