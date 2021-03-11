from ..qso import QSO
from .base import ProxyPart


class QueryPart(ProxyPart):
	__slots__ = ()
	
	attribute = '_query'
	prefix = '?'
	terminator = '#'
	cast = QSO
	
	def __get__(self, obj, cls=None):
		result = super(QueryPart, self).__get__(obj, cls)
		
		if result is None:
			result = obj._query = QSO()
		
		return result
	
	def __set__(self, obj, value):
		if value is None:
			value = ''
		
		super(QueryPart, self).__set__(obj, value)
