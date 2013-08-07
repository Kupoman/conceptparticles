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

	def __init__(self, factory, dict):
		self.x = self.y = self.z = None

		for attr, gen in dict.items():
			gen_type = gen['type']
			setattr(self, attr, factory(gen_type, gen['arguments']))

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

	def __init__(self, factory, dict):
		self.r = self.g = self.b = self.a = None

		for attr, gen in dict.items():
			gen_type = gen['type']
			del gen['type']
			if 'location' in gen:
				del gen['location']
			setattr(self, attr, factory(gen_type, gen))

	def get_value(self, x):
		value = [0, 0, 0, 0]
		if self.r:
			value[0] = self.r.get_value(x)
		if self.g:
			value[1] = self.g.get_value(x)
		if self.b:
			value[2] = self.b.get_value(x)
		if self.a:
			value[3] = self.a.get_value(x)

		return value