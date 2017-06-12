# encoding: utf-8

from __future__ import unicode_literals

from re import compile as r

from .base import ProxyPart
from ..compat import Path, str


class PathPart(ProxyPart):
	attribute = '_path'
	cast = Path
	empty = '/'
	
	def __get__(self, obj, cls=None):
		value = super(PathPart, self).__get__(obj, cls)
		
		if value is None:
			value = Path()
			obj._trailing = False
		
		return value
	
	def __set__(self, obj, value):
		try:
			obj._trailing = str(value).endswith('/')
		except:
			obj._trailing = False
		
		super(PathPart, self).__set__(obj, value)
	
	def render(self, obj, value):
		result = super(PathPart, self).render(obj, value)
		
		if result is None or result == '.':
			if not obj._host:
				return ''
			
			return self.empty
		
		if obj._trailing and not result.endswith('/'):
			result += '/'
		
		return result
