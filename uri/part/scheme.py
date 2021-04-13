from pkg_resources import iter_entry_points
from re import compile as r

from .base import Part
from ..scheme import Scheme


class SchemePart(Part):
	__slots__ = ()
	
	valid = r(r'[a-z][a-z0-9+.+-]*')
	suffix = ':'
	registry = {'': None}
	empty = ''
	
	def load(self, plugin):
		if plugin in self.registry:
			return self.registry[plugin]
		
		try:
			result, = iter_entry_points('uri.scheme', plugin)
			result = result.load()(plugin)
		except:
			result = Scheme(plugin)
		
		self.registry[plugin] = result
		
		return result
	
	def render(self, obj, value, raw=False):
		result = super(SchemePart, self).render(obj, value, raw)
		
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
