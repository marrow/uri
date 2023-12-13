from operator import attrgetter
from re import compile as r, Pattern
from typing import Any, Callable, Optional, Tuple, TypeVar, Union, Iterable, abstractmethod

from ..typing import Stringy


class Part:
	"""Descriptor protocol objects for combinatorial string parts with validation."""
	
	__slots__: Tuple[str, ...] = ()
	
	valid: Pattern = r(r'.*')
	prefix: str = ''
	suffix: str = ''
	empty: str = ''
	
	def render(self, obj, value:Optional[Stringy], raw:bool=False) -> str:
		if not value: return self.empty
		return self.prefix + str(value) + self.suffix
	
	@abstractmethod
	def __get__(self, obj, cls:Optional[type]=None):
		pass
	
	@abstractmethod
	def __set__(self, obj, value) -> None:
		pass


class ProxyPart(Part):
	__slots__: Tuple[str, ...] = ()
	
	attribute: str
	cast: Callable[[Any], str] = str
	
	def __get__(self, obj, cls=None) -> Union[str, 'ProxyPart']:
		if obj is None: return self
		return getattr(obj, self.attribute)
	
	def __set__(self, obj, value:Optional[Stringy]) -> None:
		if value == b'':
			value = None
		
		if value is not None:
			value = self.cast(value)
		
		setattr(obj, self.attribute, value)


class GroupPart(Part):
	__slots__: Tuple[str, ...] = ()
	
	attributes: Iterable[str] = ()
	sep: str = ''
	
	def __get__(self, obj, cls:Optional[type]=None) -> Union[str, 'GroupPart']:
		if obj is None: return self
		
		cls = obj.__class__
		attrs = (getattr(cls, attr).render for attr in self.attributes)
		values = (getattr(obj, attr) for attr in self.attributes)
		pipeline = (attr(obj, value) for attr, value in zip(attrs, values))
		
		return self.sep.join(i for i in pipeline if i)
	
	def __set__(self, obj, value):
		raise TypeError("{0.__class__.__name__} is not assignable.".format(self))


class BasePart(GroupPart):
	__slots__: Tuple[str, ...] = ()
	
	attributes: Tuple[str, ...] = ('scheme', 'heirarchical')
