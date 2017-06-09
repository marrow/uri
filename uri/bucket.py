# encoding: utf-8

from __future__ import unicode_literals

from collections import ItemsView, KeysView, MutableMapping, MutableSequence, ValuesView, deque, namedtuple

from .compat import SENTINEL, py2, quote_plus, str, unquote_plus


class Bucket(object):
	"""A bucket is a mutable container for an optionally named scalar value."""
	
	__slots__ = ('name', 'value', 'sep', 'valid')
	
	def __init__(self, name, value='', sep="=", strict=False):
		self.valid = True
		self.sep = sep
		
		if not value:
			if isinstance(name, str):
				if name.count(sep) > 1:
					if strict: raise ValueError("Multiple occurrences of separator {!r} in: '{!s}'".format(sep, name))
					self.valid = False
				
				name, value = self.split(name)
			
			elif isinstance(name, Bucket):
				name, value = name.name, name.value
			
			else:
				name, value = name
		
		self.name = name
		self.value = value
	
	def __eq__(self, other):
		return str(self) == str(other)
	
	def __ne__(self, other):
		return not str(self) == str(other)
	
	def split(self, string):
		name, match, value = string.partition(self.sep)
		
		name = unquote_plus(name)
		value = unquote_plus(value)
		
		return name if match else None, value if match else name
	
	def __repr__(self):
		return "{}({})".format(
				self.__class__.__name__,
				str(self)
			)
	
	if py2:
		def __repr__(self):
			return "{}({})".format(
					self.__class__.__name__,
					str(self)
				).encode('unicode-escape')
	
	def __iter__(self):
		if self.name is not None:  # XXX: Confirm that empty string is permissible.
			yield self.name
		
		yield self.value
	
	def __len__(self):
		return 1 if self.name is None else 2
	
	def __str__(self):
		# Certain symbols are explicitly allowed, ref: http://pretty-rfc.herokuapp.com/RFC3986#query
		iterator = (quote_plus(i).replace('%3F', '?').replace('%2F', '/') for i in self) if self.valid else self
		return self.sep.join(iterator)
	
	if py2:
		__unicode__ = __str__
		del __str__
