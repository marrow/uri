# encoding: utf-8

from __future__ import unicode_literals

from .base import ProxyPart, GroupPart


class HeirarchicalPart(GroupPart):
	attributes = ('auth', 'host', 'port', 'path')
