# encoding: utf-8

from __future__ import unicode_literals

from .base import ProxyPart


class FragmentPart(ProxyPart):
	__slots__ = ()
	
	attribute = '_fragment'
	prefix = '#'
