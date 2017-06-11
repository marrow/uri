# encoding: utf-8

from __future__ import unicode_literals

from collections import MutableMapping
from re import compile as r

from ..compat import Path, str, py2, urlsplit


class URIPart(object):
	__slots__ = ('parts', 'writeable')
	
	def __init__(self, parts, writeable=True):
		self.parts = parts
		self.writeable = writeable
	
	def __get__(self, obj, cls=None):
		if not cls:
			cls = obj.__class__
		
		components = []
		
		for part in self.parts:
			value = getattr(obj, part)
			part = getattr(cls, part)
			
			if value is None:
				continue
			
			components.append(part.render(obj, value))
		
		return "".join(components)
	
	def __set__(self, obj, value):
		if not self.writeable:
			raise AttributeError("Can not assign to read-only URI views.")
		
		for part in obj.__slots__:
			setattr(obj, part, None)
		
		result = urlsplit(value)
		
		for part in ('scheme', 'username', 'password', 'hostname', 'port', 'path', 'query', 'fragment'):
			pvalue = getattr(result, part)
			if pvalue is not None:
				setattr(obj, part, pvalue)
		
		obj._uri = value
