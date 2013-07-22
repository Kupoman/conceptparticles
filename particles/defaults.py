from collections import OrderedDict


from .property import Property


PROPERTIES = OrderedDict([
		("Position", Property("VECTOR", (0, 0, 0))),
		("Color", Property("COLOR", (1.0, 1.0, 1.0, 1.0))),
	])