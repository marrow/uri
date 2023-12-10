"""A type to represent, query, and manipulate a Uniform Resource Identifier."""

from importlib.metadata import metadata as _metadata, PackageNotFoundError as _NotFound
from os import getlogin
from socket import gethostname

__all__ = set(locals())  # Initial set of symbols to exclude from our module exports.

from .bucket import Bucket  # Query string fragment.
from .qso import QSO  # An object representing a whole query string.
from .uri import URI  # The primary class exposed by this package to represent a URL or URI.

try:  # Discover installed package metadata...
	_package = _metadata('uri')
	__version__ = _package.get('version')
	__author__ = f"{_package.get('author')} <{_package.get('author-email')}>"
	del _package
except _NotFound:  # ...or generate "local development" version and author information.
	__version__ = 'dev'
	__author__ = f"Local Development <{getlogin()}@{gethostname()}>"

__license__ = 'MIT'  # We could also get this from the package metadata, but it's not likely to change.
__all__ = set(i for i in locals() if not i.startswith('_')) - __all__  # Declare module exports for `import *` use.

