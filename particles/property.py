from OpenGL.GL import *


from .shaders import getProgram


TYPES = set(("VECTOR", "COLOR"))


class Property:
	def __init__(self, name, type, default, generator=None):
		self.name = name
		self.generator = generator
		self.default = default

		if type not in TYPES:
			raise ValueError("Type not in: " + str(TYPES))
		self._type = type
		self._bind_location = glGetUniformLocation(getProgram(), name.encode())

	def get_value(self, time):
		if not self.generator:
			return self.default
		return self.generator.get_value(time)

	def bind_value(self, time):
		value = self.generator.get_value(time)
		if self._type == "VECTOR":
			glUniform3f(self._bind_location, value[0], value[1], value[2])
		if self._type == "COLOR":
			glUniform4f(self._bind_location,
						value[0], value[1], value[2], value[3])
