# encoding: utf-8

from __future__ import unicode_literals

from collections import Mapping, MutableMapping, deque, namedtuple

from .bucket import Bucket
from .compat import SENTINEL, py2, quote_plus, str, unquote_plus


class QSO(object):
	"""A representation of a query string or parameter list.
	
	Acts as an ordered list of bucketed values, optionally with associated key names. Values are retrievable by index
	or by name. In the event of multiple values for a given name, a view of the associated values will be returned.
	
	Acting as both a list and dictionary may be... odd. In our case, because preserving order is the priority, most
	methods that "conflict" between the two protocols favour list-like operation, using Bucket instances as the basic
	unit of communication. This helps to preserve the original position if values are updated, as one benefit.
	Dictionary-like view methods are provided if you want to "break it down", however, again to preserve order,
	values are iterated in their original order and keys may be repeated.
	"""
	
	__slots__ = ('buckets', 'groups', 'assignment', 'separator', 'strict')
	
	def _parts(self, thing):
		if isinstance(thing, QSO):
			return (str(part) for part in thing.buckets)
		
		if isinstance(thing, Bucket):
			return (str(thing), )
		
		if isinstance(thing, Mapping):
			return thing.items()
		
		if isinstance(thing, str):
			if self.separator in thing:
				return thing.split(self.separator)
			else:
				return (thing, )
		
		return iter(thing)
	
	def __init__(self, q=None, assignment="=", separator="&", strict=False):
		self.buckets = []
		self.groups = {}
		self.assignment = assignment
		self.separator = separator
		self.strict = strict
		
		if q:
			self.extend(q)
	
	# Core Python Protocols
	
	def __repr__(self):
		return '{}("{}")'.format(self.__class__.__name__, str(self))
	
	def __str__(self):
		return self.separator.join(str(bucket) for bucket in self.buckets)
	
	# ABC Protocol Methods
	
	def __contains__(self, value):  # Container, Collection
		"""Test if a given key is set."""
		
		if isinstance(value, int):
			return 0 <= value < len(self.buckets)
		
		return value in self.groups
	
	def __iter__(self):  # Iterable, Collection
		"""Iterate the individual buckets."""
		
		return iter(self.buckets)
	
	def __len__(self):  # Sized, Collection
		"""The number of assigned buckets."""
		
		return len(self.buckets)
	
	def __reversed__(self):  # Reversible
		"""Iterate individual buckets, backwards."""
		
		return reversed(self.buckets)
	
	def __getitem__(self, index):  # Sequence
		"""Look up a bucket or buckets by numeric index or key."""
		
		if isinstance(index, int):
			return self.buckets[index]
		
		group = self.groups[index]
		
		if len(group) == 1:
			return group[0].value
		
		return (bucket.value for bucket in group)
	
	def __setitem__(self, index, value):  # MutableSequence
		"""Assign a value or bucket to a given index, or set a value by key.
		
		If there are multiple values for a key, all will be removed and a new value appended.
		"""
		
		value = Bucket(value, sep=self.assignment, strict=self.strict)
		
		if isinstance(index, int):
			bucket = self.buckets[index]
			
			if value.name is not None:
				bucket.name = value.name
			
			bucket.value = value.value
			return
		
		value.name = value.name or index
		buckets = self.groups.get(index)
		
		if buckets:
			if len(buckets) == 1:
				buckets[0].name = value.name
				buckets[0].value = value.value
				return
			
			for bucket in list(buckets):
				self.remove(bucket)
		
		self.append(value)
	
	def __delitem__(self, item):  # MutableSequence
		"""Remove a specific bucket, bucket by numeric index, or remove all buckets with the given key.
		
			>>> base = QSO("foo=27&bar&baz=42&bar&diz&name=ferret")
			>>> del base['foo']
			>>> base
			QSO("bar&baz=42&bar&diz&name=ferret")
			
			>>> del base[1]
			>>> base
			QSO("bar&bar&diz&name=ferret")
			
			>>> del base['bar']
			>>> base
			QSO("diz&name=ferret")
			
			>>> del base[base.buckets[1]]
			>>> base
			QSO("diz")
		"""
		
		if isinstance(item, int):
			item = self.buckets[item]
		
		if isinstance(item, Bucket):
			self.buckets.remove(item)
			self.groups[item.name].remove(item)
			
			if not self.groups[item.name]:  # Clean up after ourselves.
				del self.groups[item.name]
			
			return
		
		for bucket in list(self.groups[item]):
			del self[bucket]
	
	def __iadd__(self, other):  # MutableSequence
		"""Extend a current set of arguments with another set.
		
		Allows for "addition" of a variety of things, as per `QSO.extend`:
		
			>>> base = QSO("foo=27")
			>>> base += "bar"
			>>> base += {'baz': "42"}
			>>> base += ['bar', 'diz']
			>>> base += Bucket('name', 'ferret')
			>>> base
			QSO("foo=27&bar&baz=42&bar&diz&name=ferret")
		"""
		
		self.extend(other)
		return self
	
	def __eq__(self, other):  # Mapping
		return str(self) == str(other)
	
	def __ne__(self, other):  # Mapping
		return not (self == other)
	
	# ABC Public Methods
	
	def index(self, bucket, start=None, stop=None):  # Sequence
		bucket = Bucket(bucket, sep=self.assignment, strict=self.strict)
		return self.buckets.index(bucket)
	
	def count(self, thing):  # Sequence
		if not self.buckets:
			return 0
		
		if thing in self.groups:
			return len(self.groups[thing])
		
		return self.groups.get(None, []).count(Bucket(thing, sep=self.assignment, strict=self.strict))
	
	def append(self, bucket):  # MutableSequence
		bucket = Bucket(bucket, sep=self.assignment, strict=self.strict)
		self.buckets.append(bucket)
		self.groups.setdefault(bucket.name, []).append(bucket)
	
	def insert(self, index, value):  # MutableSequence
		if index < 0:  # Allow insertions at end-relative positions.
			index = len(self.buckets) + index
		index = min(len(self.buckets), index)
		
		bucket = Bucket(value, sep=self.assignment, strict=self.strict)
		
		count = 0
		for i, b in enumerate(self.buckets):
			if i >= index: break
			if b.name == bucket.name:
				count += 1
		
		self.buckets.insert(index, bucket)
		self.groups.setdefault(b.name, []).insert(count, bucket)
	
	def extend(self, *args):  # MutableSequence
		for parts in args:
			for part in self._parts(parts):
				self.append(part)
	
	def remove(self, bucket):  # MutableSequence
		del self[bucket]
	
	def pop(self, key=SENTINEL, default=SENTINEL):  # MutableSequence, MutableMapping
		if key is SENTINEL:
			key = -1
		
		if isinstance(key, int):
			try:
				bucket = self.buckets[key]
			except IndexError:
				if default is SENTINEL:
					raise KeyError()
				return default
			
			del self[bucket]
			return bucket
		
		try:
			bucket = self.groups[key].pop()
		except KeyError:
			if default is SENTINEL:
				raise
			return default
		
		self.buckets.remove(bucket)
		return bucket.value
	
	def reverse(self):  # MutableSequence
		self.buckets.reverse()
		
		for group in self.groups.values():
			group.reverse()
	
	def keys(self):  # Mapping
		return (bucket.name for bucket in self.buckets)
	
	def items(self):  # Mapping
		return (tuple(bucket) for bucket in self.buckets)
	
	def values(self):  # Mapping
		return (bucket.value for bucket in self.buckets)
	
	def get(self, bucket, default=None):  # Mapping
		if bucket in self:
			return self[bucket]
		
		return default
	
	def clear(self):  # MutableMapping
		"""Clear all values from this query string object."""
		
		del self.buckets[:]
		self.groups.clear()
	
	def update(self, *args, **kw):  # MutableMapping
		for parts in args:
			for bucket in self._parts(parts):
				bucket = Bucket(bucket, sep=self.assignment, strict=self.strict)
				self[bucket.name] = bucket.value
		
		for key in kw:
			self[key] = kw[key]


MutableMapping.register(QSO)
