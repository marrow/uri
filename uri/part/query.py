from ..typing import Iterable, Mapping, Union

from ..qso import QSO
from .base import ProxyPart


# There has to be a better placeholder for "acceptable to dict() or dict.update()".
QSOLike = Union[str, QSO, Mapping[str, str], Iterable[Iterable[str]]]


class QueryPart(ProxyPart):
	__slots__ = ()
	
	attribute = '_query'
	prefix = '?'
	terminator = '#'
	cast = QSO
	
	def __get__(self, obj, cls=None) -> QSO:
		result = super(QueryPart, self).__get__(obj, cls)
		
		if result is None:
			result = obj._query = QSO()
		
		return result
	
	def __set__(self, obj, value:QSOLike):
		if value is None:
			value = ''
		
		super(QueryPart, self).__set__(obj, value)
