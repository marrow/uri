from .base import ProxyPart


class PasswordPart(ProxyPart):
	__slots__ = ()
	
	attribute = '_password'
	prefix = ':'
