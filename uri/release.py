# encoding: utf-8

"""Release information for the uri package."""

from __future__ import unicode_literals

from collections import namedtuple

level_map = {'plan': '.dev'}

version_info = namedtuple('version_info', ('major', 'minor', 'micro', 'releaselevel', 'serial'))(2, 0, 0, 'final', 0)
version = ".".join([str(i) for i in version_info[:3]]) + \
		((level_map.get(version_info.releaselevel, version_info.releaselevel[0]) + \
		str(version_info.serial)) if version_info.releaselevel != 'final' else '')

author = namedtuple('Author', ['name', 'email'])("Alice Bevan-McGregor", 'alice@gothcandy.com')

description = "A type to represent, query, and manipulate a Uniform Resource Identifier."
url = 'https://github.com/marrow/uri/'
