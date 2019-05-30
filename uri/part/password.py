# encoding: utf-8

from __future__ import unicode_literals

from .base import ProxyPart


class PasswordPart(ProxyPart):
	__slots__ = ()
	
	attribute = '_password'
	prefix = ':'
