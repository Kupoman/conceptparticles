TYPES = {"VECTOR", "COLOR", "SCALAR"}


class Property:
	_slots_ = ["type", "generator", "default"]

	def __init__(self, type="FLOAT", default=0, generator=None):
		self.generator = generator
		self.default = default

		if type not in TYPES:
			raise ValueError("Type not in: " + str(TYPES))
		self.type = type

	def get_value(self, time):
		if not self.generator:
			return self.default
		return self.generator.get_value(time)
