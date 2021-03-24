from collections.abc import Mapping, MutableMapping
from pathlib import PurePosixPath as Path
from re import compile as r
from socket import getservbyname
from urllib.parse import urljoin

from .typing import Union, URILike, Optional
from .part.auth import AuthenticationPart, SafeAuthenticationPart
from .part.authority import AuthorityPart
from .part.base import BasePart
from .part.fragment import FragmentPart
from .part.heir import HeirarchicalPart
from .part.host import HostPart
from .part.password import PasswordPart
from .part.path import PathPart
from .part.port import PortPart
from .part.query import QueryPart
from .part.scheme import SchemePart
from .part.uri import URIPart
from .part.user import UserPart
from .scheme import Scheme, SchemeLike


class URI:
	"""An object representing a URI (absolute or relative) and its components.
	
	Acts as a mutable mapping for manipulation of query string arguments. If the query string is not URL
	"form encoded" attempts at mapping access or manipulation will fail with a ValueError. No effort is made to
	preserve original query string key order. Repeated keys will have lists as values.
	"""
	
	# Skip allocation of a dictionary per instance by pre-defining available slots.
	__slots__ = ('_scheme', '_user', '_password', '_host', '_port', '_path', '_trailing', '_query', '_fragment')
	
	__parts__ = ('scheme', 'authority', 'path', 'query', 'fragment')
	__safe_parts__ = ('scheme', '_safe_auth', 'host', 'port', 'path', 'query', 'fragment')
	__all_parts__ = {'scheme', 'user', 'password', 'host', 'port', 'path', 'query', 'fragment', 'auth', 'authority',
			'heirarchical', 'uri', 'username', 'hostname', 'authentication'}
	
	# Scalar Parts
	scheme:Union[str, Scheme] = SchemePart()
	user:str = UserPart()
	password:str = PasswordPart()
	host:str = HostPart()
	port:int = PortPart()
	path:Union[str, Path] = PathPart()
	query = QueryPart()
	fragment:Optional[str] = FragmentPart()
	
	# Compound Parts
	auth = AuthenticationPart()
	_safe_auth = SafeAuthenticationPart()
	authority = AuthorityPart()
	heirarchical = HeirarchicalPart()
	
	# Additional Compound Interfaces
	uri = URIPart(__parts__)  # Whole-URI retrieval or storage as string.
	safe_uri = URIPart(__safe_parts__, False)  # URI retrieval without password component, useful for logging.
	base = BasePart()
	origin = URIPart(('scheme', 'host', 'port'), False)
	summary = URIPart(('host', 'path'), False)
	resource = URIPart(('path', 'query', 'fragment'), False)
	defrag = URIPart(tuple([i for i in __all_parts__ if i != 'fragment']))  # Fragments are not sent to web servers.
	
	# Common Aliases
	username = user
	hostname = host
	credentials = authentication = userinfo = auth
	netloc = authority
	
	# Factories
	
	@classmethod
	def from_wsgi(URI, environ) -> 'URI':
		if hasattr(environ, 'environ'):  # Incidentally support passing of a variety of Request object wrappers.
			environ = environ.environ
		
		scheme = environ['wsgi.url_scheme']
		
		uri = URI(
				scheme = scheme,
				host = environ['SERVER_NAME'],
				path = environ['SCRIPT_NAME'] + environ['PATH_INFO'],
				query = environ['QUERY_STRING']
			)
		
		# Handled this way to automatically elide default port numbers.
		service = getservbyname(scheme)
		port = int(environ['SERVER_PORT'])
		if not service or service != port: uri.port = port
		
		return uri
	
	# Shortcuts
	
	@property
	def qs(self) -> str:
		query = self.query
		return str(query) if query else ""
	
	@qs.setter
	def qs(self, value) -> None:
		self.query = value
	
	# Python Object Protocol
	
	def __init__(self, _uri:Optional[URILike]=None, **parts) -> None:
		"""Initialize a new URI from a passed in string and/or named parts.
		
		If both a base URI and parts are supplied than the parts will override those present in the URI.
		"""
		
		if hasattr(_uri, '__link__'):  # We utilize a custom object protocol to retrieve links to things.
			_uri = _uri.__link__
			
			# To allow for simpler cases, this attribute does not need to be callable.
			if callable(_uri): _uri = _uri()
		
		if hasattr(_uri, 'as_uri'):  # Support pathlib method protocol.
			_uri = _uri.as_uri()
		
		self.uri = _uri  # If None, this will also handle setting defaults.
		
		if parts:  # If not given a base URI, defines a new URI, otherwise update the given URI.
			for part, value in parts.items():
				if part not in self.__all_parts__:
					raise TypeError("Unknown URI component: " + part)
				
				setattr(self, part, value)
	
	# Python Datatype Protocols
	
	def __repr__(self):
		"""Return a "safe" programmers' representation that omits passwords."""
		
		return "{0}('{1}')".format(self.__class__.__name__, self.safe_uri)
	
	def __str__(self):
		"""Return the Unicode text representation of this URI, including passwords."""
		
		return self.uri
	
	def __bytes__(self):
		"""Return the binary string representation of this URI, including passwords."""
		
		return self.uri.encode('utf-8')
	
	# Python Comparison Protocol
	
	def __eq__(self, other):
		"""Compare this URI against another value."""
		
		if not isinstance(other, self.__class__):
			other = self.__class__(other)
		
		# Because things like query string argument order may differ, but still be equivalent...
		for part in self.__parts__:
			ours = getattr(self, part, None)
			theirs = getattr(other, part, None)
			
			if ours != theirs:
				return False
		
		return True
	
	def __ne__(self, other):
		"""Inverse comparison support."""
		
		return not self == other
	
	def __bool__(self):
		"""Truthyness comparison."""
		
		return bool(self.uri)
	
	# Python Mapping Protocol
	
	def __getitem__(self, name):
		"""Shortcut for retrieval of a query string argument or syntax sugar to apply a username:password pair.
		
		For example:
		
			url = URI("http://example.com/hello?name=world")
			url['name'] == 'world'
		
		Alternatively:
		
			url = URI("http://example.com/hello")
			authd_url = url['username':'password']
		"""
		
		if isinstance(name, slice):
			self = self.__class__(str(self))  # We do not mutate ourselves; instead, mutate a clone.
			self.user, self.password = name.start, name.stop
			return self
		
		return self.query[name]
	
	def __setitem__(self, name, value):
		"""Shortcut for (re)assignment of query string arguments."""
		
		self.query[name] = str(value)
	
	def __delitem__(self, name):
		"""Shortcut for removal of a query string argument."""
		
		del self.query[name]
	
	def __iter__(self):
		"""Retrieve the query string argument names."""
		
		return iter(self._query)
	
	def __len__(self):
		"""The length of the URI as a string."""
		return len(self.uri)
	
	# Path-like behaviours.
	
	def __div__(self, other):
		sother = str(other)
		
		if sother == '.':  # This URI without fragment or query.
			return self.__class__(self, query=None, fragment=None)
		
		if sother.startswith('#'):  # Fragment change only.
			return self.__class__(self, fragment=other[1:])
		
		if '://' in sother:  # Whole-uri switch.
			return self.__class__(other)
		
		# Otherwise resolve path.
		base = str(self.path) or '.'
		trailing = False if base in ('/', '.') else self._trailing
		
		if base == '.':
			base = '/'
		
		elif trailing:
			base += '/'
		
		return self.__class__(self, path=urljoin(base, sother), query=None, fragment=None)
	
	__idiv__ = __div__
	__truediv__ = __div__
	
	def __floordiv__(self, other):
		other = str(other)
		
		if '//' in other:
			_, _, other = other.partition('//')
		
		return self.__class__(str(self.scheme) + "://" + other)
	
	__ifloordiv__ = __floordiv__
	
	# Support Protocols
	
	__link__ = __str__  # Various
	make_uri = __str__  # Path
	
	def __html__(self):  # Markupsafe
		"""Return an HTML representation of this link.
		
		A link to http://example.com/foo/bar will result in:
		
			<a href="http://example.com/foo/bar">example.com/foo/bar</a>
		"""
		
		from markupsafe import escape
		
		return '<a href="{address}">{summary}</a>'.format(
				address = escape(self.uri),
				summary = escape(self.summary),
			)
	
	def geturl(self):  # API compatibility with urllib.
		return str(self)
	
	@property
	def relative(self):
		"""Identify if this URI is relative to some "current context".
		
		For example, if the protocol is missing, it's protocol-relative. If the host is missing, it's host-relative, etc.
		"""
		
		scheme = self.scheme
		
		if not scheme:
			return True
		
		return scheme.is_relative(self)
	
	def resolve(self, uri=None, **parts):
		"""Attempt to resolve a new URI given an updated URI, partial or complete."""
		
		if uri:
			result = self.__class__(urljoin(str(self), str(uri)))
		else:
			result = self.__class__(self)
		
		for part, value in parts.items():
			if part not in self.__all_parts__:
				raise TypeError("Unknown URI component: " + part)
			
			setattr(result, part, value)
		
		return result


MutableMapping.register(URI)
