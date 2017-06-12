# encoding: utf-8

from __future__ import unicode_literals

from pkg_resources import iter_entry_points

from .base import Part
from ..compat import py2, r
from ..scheme import Scheme


class SchemePart(Part):
	valid = r(r'[a-z][a-z0-9+.+-]*')
	suffix = ':'
	registry = {'': None}
	
	def load(self, plugin):
		if plugin in self.registry:
			return self.registry[plugin]
		
		# TODO: Entry point namespace use for plugin discovery.
		
		try:
			result, = iter_entry_points('uri.scheme', plugin)
			result = result.load()(plugin)
		except:
			result = Scheme(plugin)
		
		self.registry[plugin] = result
		
		return result
	
	def render(self, obj, value):
		result = super(SchemePart, self).render(obj, value)
		
		if obj._scheme and obj.scheme.slashed:
			result = result + '//'
		
		return result
	
	def __get__(self, obj, cls=None):
		if obj is None: return self
		scheme = obj._scheme
		
		return self.load(scheme)
	
	def __set__(self, obj, value):
		obj._scheme = Scheme(value).name