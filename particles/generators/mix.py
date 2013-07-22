from collections import OrderedDict


from .common import Generator

class Mix3(Generator):
	out_type = "VECTOR"

	type_map =	OrderedDict((
					("x", "GENERATOR_SCALAR"),
					("y", "GENERATOR_SCALAR"),
					("z", "GENERATOR_SCALAR"),
				))

	__slots__ = type_map.keys()

	def __init__(self, factory, n1="", d1={}, n2="", d2={}, n3="", d3={}):
		self.x = self.y = self.z = None

		if n1:
			self.x = factory(n1, d1)
		if n2:
			self.y = factory(n2, d2)
		if n3:
			self.z = factory(n3, d3)

	def get_value(self, x):
		value = [0, 0, 0]
		if self.x:
			value[0] = self.x.get_value(x)
		if self.y:
			value[1] = self.y.get_value(x)
		if self.z:
			value[2] = self.z.get_value(x)

		return value

class Mix4(Generator):
	out_type = "COLOR"

	type_map =	OrderedDict((
					("r", "GENERATOR_SCALAR"),
					("g", "GENERATOR_SCALAR"),
					("b", "GENERATOR_SCALAR"),
					("a", "GENERATOR_SCALAR"),
				))

	__slots__ = type_map.keys()

	def __init__(self, factory, n1="", d1={}, n2="", d2={}, n3="", d3={}, n4="", d4={}):
		self.r = self.g = self.b = self.a = None

		if n1:
			self.r = factory(n1, d1)
		if n2:
			self.g = factory(n2, d2)
		if n3:
			self.b = factory(n3, d3)
		if n4:
			self.b = factory(n4, d4)

	def get_value(self, x):
		value = [0, 0, 0, 0]
		if self.r:
			value[0] = self.r.get_value(x)
		if self.g:
			value[1] = self.g.get_value(x)
		if self.b:
			value[2] = self.b.get_value(x)
		if self.a:
			value[2] = self.a.get_value(x)

		return value