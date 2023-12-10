from operator import attrgetter
from re import compile as r


class Part:
	"""Descriptor protocol objects for combinatorial string parts with validation."""
	
	__slots__ = ()
	
	valid = r(r'.*')
	prefix = ''
	suffix = ''
	empty = ''
	
	def render(self, obj, value):
		if not value: return self.empty
		return self.prefix + str(value) + self.suffix


class ProxyPart(Part):
	__slots__ = ()
	
	attribute = None
	cast = str
	
	def __get__(self, obj, cls=None):
		if obj is None: return self
		return getattr(obj, self.attribute)
	
	def __set__(self, obj, value):
		if value == b'':
			value = None
		
		if value is not None:
			value = self.cast(value)
		
		setattr(obj, self.attribute, value)


class GroupPart(Part):
	__slots__ = ('_getters', '_join')
	
	attributes = ()
	sep = ''
	
	def __get__(self, obj, cls=None):
		if obj is None: return self
		
		cls = obj.__class__
		attrs = (getattr(cls, attr).render for attr in self.attributes)
		values = (getattr(obj, attr) for attr in self.attributes)
		pipeline = (attr(obj, value) for attr, value in zip(attrs, values))
		
		return self.sep.join(i for i in pipeline if i)
	
	def __set__(self, obj, value):
		raise TypeError("{0.__class__.__name__} is not assignable.".format(self))


class BasePart(GroupPart):
	__slots__ = ()
	
	attributes = ('scheme', 'heirarchical')
