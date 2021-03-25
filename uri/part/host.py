from socket import inet_pton, AF_INET6, error as SocketError

from .base import ProxyPart


class HostPart(ProxyPart):
	__slots__ = ()
	
	attribute = '_host'
	
	def render(self, obj, value):
		result = super(HostPart, self).render(obj, value)
		
		try:
			result.encode('ascii')
		except UnicodeEncodeError:
			result = result.encode('idna').decode('ascii')
		
		if result:
			try:  # Identify and armour IPv6 address literals.
				inet_pton(AF_INET6, value)
			except SocketError:
				pass
			else:
				result = '[' + result + ']'
		
		return result
	
	def __set__(self, obj, value):
		if isinstance(value, bytes):
			value = value.decode('idna')
		elif value.startswith('xn--'):
			value = value.encode('ascii').decode('idna')
		
		super().__set__(obj, value)
