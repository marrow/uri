# encoding: utf-8

from __future__ import unicode_literals

from .compat import str, py2


class Scheme(object):
	__slots__ = ('name', )
	
	slashed = False  # Do NOT include // separator between scheme and remainder.
	
	def __init__(self, name):
		self.name = str(name).strip().lower()
	
	def __eq__(self, other):
		if isinstance(other, str):
			return self.name == other
		
		if isinstance(other, self.__class__):
			return self is other
	
	def __neq__(self, other):
		return not (self == other)
	
	def __bytes__(self):
		return self.name.encode('ascii')
	
	def __str__(self):
		return self.name
	
	if py2:
		__unicode__ = __str__
		del __str__
	
	def is_relative(self, uri):
		return False


class URLScheme(Scheme):
	slashed = True  # DO include // separator between scheme and remainder.
	
	def is_relative(self, uri):
		return not uri._host or not uri._path.is_absolute()
