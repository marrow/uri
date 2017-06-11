# encoding: utf-8

from __future__ import unicode_literals

from socket import inet_pton, AF_INET6, error as SocketError

from .base import ProxyPart


class HostPart(ProxyPart):
	attribute = '_host'
	
	def render(self, obj, value):
		result = super(HostPart, self).render(obj, value)
		
		if result:
			try:  # Identify and armour IPv6 address literals.
				inet_pton(AF_INET6, value)
			except SocketError:
				pass
			else:
				result = '[' + result + ']'
		
		return result
