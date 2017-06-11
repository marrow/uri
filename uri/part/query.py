# encoding: utf-8

from __future__ import unicode_literals

from ..compat import str
from ..qso import QSO
from .base import ProxyPart


class QueryPart(ProxyPart):
	attribute = '_query'
	prefix = '?'
	terminator = '#'
	cast = QSO
