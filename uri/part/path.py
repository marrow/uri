# encoding: utf-8

from __future__ import unicode_literals

from re import compile as r

from .base import ProxyPart
from ..compat import Path, str


class PathPart(ProxyPart):
	attribute = '_path'
	cast = Path
	empty = '/'
	
	def render(self, obj, value):
		result = super(PathPart, self).render(obj, value)
		
		if result == '.':
			if not obj._host:
				return ''
			return self.empty
		
		return result
