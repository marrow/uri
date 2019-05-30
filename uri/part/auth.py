# encoding: utf-8

from __future__ import unicode_literals

from .base import ProxyPart, GroupPart


class AuthenticationPart(GroupPart):
	__slots__ = ()
	
	attributes = ('user', 'password')
	suffix = '@'


class SafeAuthenticationPart(ProxyPart):
	__slots__ = ()
	
	attribute = 'user'
	suffix = '@'
