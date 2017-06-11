# encoding: utf-8

from __future__ import unicode_literals

from .base import ProxyPart


class FragmentPart(ProxyPart):
	attribute = '_fragment'
	prefix = '#'
