class Linear:
	__slots__ = ["m", "b"]
	
	def __init__(self, m=1.0, b=0.0):
		self.m = m
		self.b = b
		
	def get_value(self, x):
		return self.m * x + self.b