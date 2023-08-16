"""A type to represent, query, and manipulate a Uniform Resource Identifier."""

from importlib.metadata import metadata as _metadata, PackageNotFoundError as _NotFound
from pathlib import PurePosixPath as Path

__all__ = set(locals())

from .bucket import Bucket
from .qso import QSO
from .uri import URI

try:
	_package = _metadata('uri')
	__version__ = _package.get('version')
	__author__ = _package.get('author-email')
	del _package
except _NotFound:
	__version__ = 'dev'
	__author__ = "Local Development"

__all__ = set(i for i in locals() if not i.startswith('_')) - __all__
__license__ = 'MIT'

