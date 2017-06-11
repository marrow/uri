# encoding: utf-8

from __future__ import unicode_literals

from .base import ProxyPart, GroupPart


class AuthenticationPart(GroupPart):
	attributes = ('user', 'password')
	suffix = '@'


class SafeAuthenticationPart(ProxyPart):
	attribute = 'user'
	suffix = '@'
