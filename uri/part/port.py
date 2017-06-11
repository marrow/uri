# encoding: utf-8

from __future__ import unicode_literals

from .base import ProxyPart


class PortPart(ProxyPart):
	attribute = '_port'
	prefix = ':'
	cast = int
