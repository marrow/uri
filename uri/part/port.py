# encoding: utf-8

from __future__ import unicode_literals

from .base import ProxyPart


class PortPart(ProxyPart):
	__slots__ = ()
	
	attribute = '_port'
	prefix = ':'
	cast = int
