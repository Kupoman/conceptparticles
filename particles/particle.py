from ctypes import *


class GPUPARTICLE(Structure):
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
				

class CPUPARTICLE(Structure):
	_fields_ = [
					("life", c_int),
					("time", c_int),
				]