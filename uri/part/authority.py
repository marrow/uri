# encoding: utf-8

from __future__ import unicode_literals

from .base import GroupPart


class AuthorityPart(GroupPart):
	__slots__ = ()
	
	attributes = ('auth', 'host', 'port')
