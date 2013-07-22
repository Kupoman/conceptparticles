from collections import OrderedDict


from .common import Generator


class Constant(Generator):
	out_type = "SCALAR"

	type_map =	OrderedDict((
					("value", "SCALAR"),
				))

	__slots__ = type_map.keys()

	def __init__(self, value=0):
		self.value = value

	def get_value(self, x):
		return self.value

		
class Constant3(Constant):
	out_type = "VECTOR"

	type_map =	OrderedDict((
					("value", "VECTOR"),
				))

	def __init__(self, value=(0, 0, 0)):
		self.value = value

		
class Constant4(Constant):
	out_type = "COLOR"

	type_map =	OrderedDict((
					("value", "COLOR"),
				))

	def __init__(self, value=(0, 0, 0, 0)):
		self.value = value