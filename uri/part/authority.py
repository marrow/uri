# encoding: utf-8

from __future__ import unicode_literals

from .base import GroupPart


class AuthorityPart(GroupPart):
	attributes = ('auth', 'host', 'port')
