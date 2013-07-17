from ctypes import *

class RPARTICLE(Structure):
	_fields_ = [
					("x", c_float),
					("y", c_float),
					("z", c_float),
					("r", c_float),
					("g", c_float),
					("b", c_float),
					("a", c_float),
					("pad", c_float)
				]