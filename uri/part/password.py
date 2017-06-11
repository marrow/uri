# encoding: utf-8

from __future__ import unicode_literals

from .base import ProxyPart


class PasswordPart(ProxyPart):
	attribute = '_password'
	prefix = ':'
