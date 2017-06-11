# encoding: utf-8

from __future__ import unicode_literals

from .base import Part
from ..compat import py2, r
from ..scheme import Scheme


class SchemePart(Part):
	valid = r(r'[a-z][a-z0-9+.+-]*')
	suffix = ':'
	registry = {'': None}
	
	def load(self, plugin):
		if not plugin:
			if plugin in self.registry:
				return self.registry[plugin]
			
			return plugin
		
		# TODO: Entry point namespace use for plugin discovery.
		
		self.registry[plugin] = plugin = Scheme(plugin)  # Order is important here, due to label re-use.
		
		return plugin
	
	def __get__(self, obj, cls=None):
		if obj is None: return self
		scheme = obj._scheme
		
		return self.load(scheme)
	
	def __set__(self, obj, value):
		obj._scheme = Scheme(value).name
