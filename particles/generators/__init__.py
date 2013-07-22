from .linear import Linear
from .mix import Mix3, Mix4
from .constant import Constant, Constant3, Constant4


GENERATORS = {
				"LINEAR",
				"MIX3",
				"MIX4",
				"CONSTANT",
				"CONSTANT3",
				"CONSTANT4",
				}

def get_generator(name, args):
	if name in GENERATORS:
		class_name = name[0] + name[1:].lower()
		gen = globals()[class_name]
		if class_name.startswith("Mix"):
			gen = gen(get_generator, args)
		else:
			gen = gen(**args)
			
		return gen
	
	raise ValueError("%s is not a valid generator" % name)