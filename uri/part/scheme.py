from importlib.metadata import entry_points
from typing import ClassVar, Dict, Optional
from re import compile as r, Pattern

from .base import Part
from ..scheme import Scheme


class SchemePart(Part):
	__slots__: tuple = ()  # Do not populate a __dict__ dictionary attribute; only allocate space for these.
	
	registry: ClassVar[Dict[str, Optional[Scheme]]] = {'': None}
	suffix: str = ':'  # Protocol suffix when utilized as part of a complete URI; e.g. ':' or '://'.
	valid: Pattern = r(r'[a-z][a-z0-9+.+-]*')  # Protocol/scheme name validated when run unoptimized.
	
	def load(self, plugin:str) -> Scheme:
		assert self.valid.match(plugin), f"Invalid plugin name: {plugin!r}"
		if plugin in self.registry: return self.registry[plugin]  # Short circuit if we've seen this before.
		
		# If we haven't, attempt to load the explicit Scheme subclass to utilize for this named scheme.
		try: result = entry_points(group='uri.scheme')[plugin].load()
		except KeyError: result = Scheme(plugin)  # Can't look up by registered name? It's generic.
		else: result = result(plugin)  # Otherwise, instantiate the subclass, informing it of its name.
		
		self.registry[plugin] = result  # Record the instance in a local registry / cache.
		
		return result
	
	def render(self, obj, value) -> str:
		result = super(SchemePart, self).render(obj, value)
		
		if obj._scheme and obj.scheme.slashed:
			result = result + '//'
		
		elif not obj._scheme and obj.authority:
			result = '//'
		
		return result
	
	def __get__(self, obj, cls=None):
		if obj is None: return self
		scheme = obj._scheme
		
		if scheme is not None:
			scheme = self.load(scheme)
		
		return scheme
	
	def __set__(self, obj, value):
		if isinstance(value, bytes):
			value = value.decode('ascii')
		
		if not value:
			obj._scheme = None
			return
		
		obj._scheme = Scheme(value).name
