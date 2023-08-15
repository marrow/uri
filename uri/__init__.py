"""A type to represent, query, and manipulate a Uniform Resource Identifier."""

from pathlib import PurePosixPath as Path

from .bucket import Bucket
from .qso import QSO
from .uri import URI

__version__ = ''

__all__ = [
		'Path',
		'Bucket',
		'QSO',
		'URI',
	]  # TODO: Re-watch that Python import internals presentation for the semi-auto way to do this.
