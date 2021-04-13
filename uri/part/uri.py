from collections.abc import MutableMapping
from re import compile as r
from urllib.parse import urlsplit


class URIPart:
	__slots__ = ('parts', 'writeable', 'raw')
	
	def __init__(self, parts, writeable=True, raw=False):
		self.parts = parts
		self.writeable = writeable
		self.raw = raw
	
	def __get__(self, obj, cls=None):
		components = []
		
		for part in self.parts:
			value = getattr(obj, part)
			part = getattr(cls, part)
			
			components.append(part.render(obj, value, self.raw))
		
		return "".join(components)
	
	def __set__(self, obj, value):
		if not self.writeable:
			raise AttributeError("Can not assign to read-only URI views.")
		
		for part in obj.__slots__:
			setattr(obj, part, None)
		
		if not value:
			return
		
		result = urlsplit(str(value))
		
		obj._trailing = result.path.endswith('/')
		
		for part in ('scheme', 'username', 'password', 'hostname', 'port', 'path', 'query', 'fragment'):
			pvalue = getattr(result, part)
			if pvalue:
				setattr(obj, part, pvalue)
