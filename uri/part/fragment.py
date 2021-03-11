from .base import ProxyPart


class FragmentPart(ProxyPart):
	__slots__ = ()
	
	attribute = '_fragment'
	prefix = '#'
