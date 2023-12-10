class Scheme:
	__slots__ = ('name', )
	
	slashed = False  # Do NOT include // separator between scheme and remainder.
	
	def __init__(self, name):
		self.name = str(name).strip().lower()
	
	def __eq__(self, other):
		if isinstance(other, str):
			return self.name == other
		
		if isinstance(other, self.__class__):
			return self is other
	
	def __hash__(self):
		return hash(self.name)
	
	def __neq__(self, other):
		return not (self == other)
	
	def __bytes__(self):
		return self.name.encode('ascii')
	
	def __str__(self):
		return self.name
	
	def __repr__(self):
		return f"{self.__class__.__name__}('{self.name}')"
	
	def is_relative(self, uri):
		return False


class URLScheme(Scheme):
	__slots__ = ()
	
	slashed = True  # DO include // separator between scheme and remainder.
	
	def is_relative(self, uri):
		return not uri._host or not uri._path.is_absolute()
