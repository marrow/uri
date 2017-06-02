# encoding: utf-8

from __future__ import unicode_literals

from collections import namedtuple, deque, MutableSequence, MutableMapping, ItemsView, KeysView, ValuesView

from .compat import SENTINEL, str, py2



class Bucket(object):
	"""A bucket is a mutable container for an optionally named scalar value."""
	
	__slots__ = ('name', 'value', 'sep')
	
	def __init__(self, name, value='', sep="=", strict=False):
		if not value:
			name, value = self.split(name, sep, strict)
		
		self.name = name
		self.value = value
		self.sep = sep
		
		if strict and (sep in name or sep in value):
			raise ValueError("Multiple occurrences of separator {!r} in: {!s}".format(sep, self))
	
	def __eq__(self, other):
		return str(self) == str(other)
	
	def __ne__(self, other):
		return not str(self) == str(other)
	
	@classmethod
	def split(cls, string, sep="=", strict=False):
		if strict and string.count(sep) > 1:
			raise ValueError("Multiple occurrences of separator {!r} in: {!r}".format(sep, string))
		
		name, match, value = string.partition(sep)
		return name if match else None, value if match else name
	
	@property
	def valid(self):
		return not (self.name and self.sep in self.name) and self.sep not in self.value
	
	def __repr__(self):
		return "{}({})".format(
				self.__class__.__name__,
				str(self)
			)
	
	def __iter__(self):
		if self.name is not None:  # XXX: Confirm that empty string is permissible.
			yield self.name
		
		yield self.value
	
	def __len__(self):
		return 1 if self.name is None else 2
	
	def __str__(self):
		return self.sep.join(self)
	
	if py2:
		__unicode__ = __str__
		del __str__
