from collections import OrderedDict


from .property import Property


PROPERTIES = OrderedDict([
		("Emit Rate", Property("SCALAR", 0.1)),
		("Position", Property("VECTOR", (0, 0, 0))),
		("Color", Property("COLOR", (1.0, 1.0, 1.0, 1.0))),
	])