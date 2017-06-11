# encoding: utf-8

from __future__ import unicode_literals

from re import compile as r

from .base import ProxyPart
from ..compat import Path, str


class PathPart(ProxyPart):
	attribute = '_path'
	cast = Path
