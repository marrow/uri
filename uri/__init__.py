"""A type to represent, query, and manipulate Uniform Resource Identifiers."""

from importlib.metadata import metadata as _metadata, PackageNotFoundError as _NotFound
from os import getlogin
from socket import gethostname

__all__ = list(locals())  # Initial set of symbols to exclude from our module exports.

from pathlib import PurePosixPath as Path

from .bucket import Bucket  # Query string fragment.
from .qso import QSO  # An object representing a whole query string.
from .uri import URI  # The primary class exposed by this package to represent a URL or URI.

try:  # Discover installed package metadata...
	_package = _metadata('uri')
	__version__ = ", ".join(_package.get_all('version'))
	__author__ = "\n".join(_package.get_all('author-email'))

except _NotFound:  # ...or generate "local development" version and author information.
	__version__ = 'dev'
	__author__ = f"Local Development <{getlogin()}@{gethostname()}>"

__license__ = "MIT"
__all__ = list(set(i for i in locals() if not i.startswith('_')) - set(__all__))  # Declare module exports for `import *` use.

