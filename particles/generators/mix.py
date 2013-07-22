from .common import Generator

class Mix3(Generator):
	__slots__ = ["gen1", "gen2", "gen3"]
	
	def __init__(self, factory, n1="", d1={}, n2="", d2={}, n3="", d3={}):
		self.gen1 = self.gen2 = self.gen3 = None
		
		if n1:
			self.gen1 = factory(n1, d1)
		if n2:
			self.gen2 = factory(n2, d2)
		if n3:
			self.gen3 = factory(n3, d3)
			
	def get_value(self, x):
		value = [0, 0, 0]
		if self.gen1:
			value[0] = self.gen1.get_value(x)
		if self.gen2:
			value[1] = self.gen2.get_value(x)
		if self.gen3:
			value[2] = self.gen3.get_value(x)
			
		return value