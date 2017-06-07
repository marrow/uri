# encoding: utf-8

try:  # Minimal compatibility requirements.
	str = unicode
	py2 = True
except:
	str = str
	py2 = False

try:
	from html import escape
except ImportError:  # Adapt to locations on legacy versions.
	from cgi import escape

try:
	from urllib.parse import urljoin, urlsplit, quote_plus, unquote_plus
except ImportError:  # Adapt to locations on legacy versions.
	from urlparse import urljoin, urlsplit
	from urllib import quote_plus, unquote_plus

try:
	from pathlib import PurePosixPath as Path
except ImportError:
	from pathlib2 import PurePosixPath as Path

from re import compile as r

SENTINEL = object()
