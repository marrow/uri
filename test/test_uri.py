# encoding: utf-8

from __future__ import unicode_literals

import pytest

from uri.compat import SENTINEL, Path
from uri.uri import URI

URI_COMPONENTS = [
		('http://', dict(
				relative = True,
				scheme = 'http',
				base = 'http://',
				path = Path('.'),
			)),
		('https://', dict(
				relative = True,
				scheme = 'https',
				base = 'https://',
				path = Path('.'),
			)),
		('/foo', dict(
				relative = True,
				path = Path('/foo'),
				base = '/foo',
				summary = '/foo',
				heirarchical = '/foo',
			)),
		('http://user:pass@example.com/over/there?name=ferret#anchor', dict(
				authority = 'user:pass@example.com',
				fragment = 'anchor',
				user = 'user',
				username = 'user',
				password = 'pass',
				heirarchical = 'user:pass@example.com/over/there',
				host = 'example.com',
				path = Path('/over/there'),
				query = 'name=ferret',
				scheme = 'http',
				authentication = 'user:pass',
				auth = 'user:pass',
				base = 'http://user:pass@example.com/over/there',
				summary = 'example.com/over/there',
				relative = False,
			)),
		
		# From Wikipedia - https://en.wikipedia.org/wiki/Query_string
		('http://example.com/over/there?name=ferret', dict(
				authority = 'example.com',
				heirarchical = 'example.com/over/there',
				host = 'example.com',
				path = Path('/over/there'),
				query = 'name=ferret',
				base = 'http://example.com/over/there',
				scheme = 'http',
				summary = 'example.com/over/there',
				relative = False,
			)),
		('http://example.com/path/to/page?name=ferret&color=purple', dict(
				authority = 'example.com',
				heirarchical = 'example.com/path/to/page',
				host = 'example.com',
				path = Path('/path/to/page'),
				query = 'name=ferret&color=purple',
				scheme = 'http',
				base = 'http://example.com/path/to/page',
				summary = 'example.com/path/to/page',
				relative = False,
			)),
		
		# RFC 3986 (URI) - http://pretty-rfc.herokuapp.com/RFC3986
		('ftp://ftp.is.co.za/rfc/rfc1808.txt', dict(
				authority = 'ftp.is.co.za',
				host = 'ftp.is.co.za',
				path = Path('/rfc/rfc1808.txt'),
				heirarchical = 'ftp.is.co.za/rfc/rfc1808.txt',
				scheme = 'ftp',
				base = 'ftp://ftp.is.co.za/rfc/rfc1808.txt',
				summary = 'ftp.is.co.za/rfc/rfc1808.txt',
				relative = False,
			)),
		('ldap://[2001:db8::7]/c=GB?objectClass?one', dict(
				authority = '[2001:db8::7]',
				path = Path('/c=GB'),
				scheme = 'ldap',
				query = 'objectClass?one',
				host = '2001:db8::7',
				heirarchical = '[2001:db8::7]/c=GB',
				base = 'ldap://[2001:db8::7]/c=GB',
				summary = '[2001:db8::7]/c=GB',
				relative = False,
			)),
		('http://www.ietf.org/rfc/rfc2396.txt', dict(
				authority = 'www.ietf.org',
				scheme = 'http',
				host = 'www.ietf.org',
				path = Path('/rfc/rfc2396.txt'),
				heirarchical = 'www.ietf.org/rfc/rfc2396.txt',
				base = 'http://www.ietf.org/rfc/rfc2396.txt',
				summary = 'www.ietf.org/rfc/rfc2396.txt',
				relative = False,
			)),
		('mailto:John.Doe@example.com', dict(
				scheme = 'mailto',
				path = Path('John.Doe@example.com'),
				heirarchical = 'John.Doe@example.com',
				summary = 'John.Doe@example.com',
				base = 'mailto:John.Doe@example.com',
				relative = False,
			)),
		('tel:+1-816-555-1212', dict(
				scheme = 'tel',
				path = Path('+1-816-555-1212'),
				heirarchical = '+1-816-555-1212',
				summary = '+1-816-555-1212',
				base = 'tel:+1-816-555-1212',
				relative = False,
			)),
		('telnet://192.0.2.16:80/', dict(
				port = 80,
				scheme = 'telnet',
				host = '192.0.2.16',
				authority = '192.0.2.16:80',
				path = Path('/'),
				heirarchical = '192.0.2.16:80/',
				summary = '192.0.2.16/',
				base = 'telnet://192.0.2.16:80/',
				relative = False,
			)),
		('urn:oasis:names:specification:docbook:dtd:xml:4.1.2', dict(
				scheme = 'urn',
				path = Path('oasis:names:specification:docbook:dtd:xml:4.1.2'),  # TODO
				heirarchical = 'oasis:names:specification:docbook:dtd:xml:4.1.2',
				summary = 'oasis:names:specification:docbook:dtd:xml:4.1.2',
				base = 'urn:oasis:names:specification:docbook:dtd:xml:4.1.2',
				relative = False,
			)),
	]

for _uri, _parts in URI_COMPONENTS:
	_parts['uri'] = _uri
	if 'query' in _parts: _parts['qs'] = _parts['query']
	if 'host' in _parts: _parts['hostname'] = _parts['host']


@pytest.fixture
def instance():
	return URI('http://user:pass@example.com/over/there?name=ferret#anchor')


@pytest.fixture
def empty():
	return URI('http://example.com/over/there')


@pytest.mark.parametrize('string,attributes', URI_COMPONENTS)
class TestURI(object):
	def test_truthiness(self, string, attributes):
		instance = URI(string)
		assert instance
	
	def test_identity(self, string, attributes):
		instance = URI(string)
		assert str(instance) == attributes['uri']
	
	def test_identity_bytes(self, string, attributes):
		instance = URI(string)
		assert bytes(instance) == attributes['uri'].encode('utf-8')
	
	def test_identity_comparison(self, string, attributes):
		instance = URI(string)
		assert instance == attributes['uri']
	
	def test_inverse_bad_comparison(self, string, attributes):
		instance = URI(string)
		assert instance != "fnord"
	
	def test_length(self, string, attributes):
		instance = URI(string)
		assert len(instance) == len(string)
	
	@pytest.mark.parametrize('component', URI.__all_parts__ | {'base', 'qs', 'summary', 'relative'})
	def test_component(self, string, attributes, component):
		instance = URI(string)
		value = getattr(instance, component, SENTINEL)
		
		if component not in attributes:
			assert value in (None, SENTINEL, '')
			return
		
		assert value == attributes[component]


class TestURIBasics(object):
	def test_uri_error(self):
		with pytest.raises(TypeError):
			URI(foo="bar")
	
	def test_empty(self):
		instance = URI()
		assert str(instance) == ""
		assert not instance
	
	def test_html_representation(self, instance):
		markupsafe = pytest.importorskip('markupsafe')
		
		html = markupsafe.escape(instance)
		expect = '<a href="http://user:pass@example.com/over/there?name=ferret#anchor">example.com/over/there</a>'
		
		assert html == expect
	
	def test_protocol_relative_shortcut(self, instance):
		https = URI("https://")
		
		instance = https // instance
		assert str(instance) == "https://user:pass@example.com/over/there?name=ferret#anchor"
	
	def test_rooted(self, instance):
		instance = instance / "/foo"
		assert str(instance) == "http://user:pass@example.com/foo"
	
	def test_relative(self, instance):
		instance = instance / "foo"
		assert str(instance) == "http://user:pass@example.com/over/foo"
	
	def test_relative_assignment(self, instance):
		instance /= "bar"
		assert str(instance) == "http://user:pass@example.com/over/bar"
	
	def test_resolution_by_uri(self, instance):
		assert str(instance.resolve('/baz')) == "http://user:pass@example.com/baz"
		assert str(instance.resolve('baz')) == "http://user:pass@example.com/over/baz"
	
	def test_resolution_overriding(self, instance):
		expect = "http://example.com/over/there?name=ferret#anchor"
		assert str(instance.resolve(user=None, password=None)) == expect
	
	def test_resolution_error(self, instance):
		with pytest.raises(TypeError):
			instance.resolve(unknown="fnord")
	
	def test_qs_assignment(self):
		instance = URI("http://example.com")
		assert str(instance) == "http://example.com/"
		
		instance.qs = "foo=bar"
		assert str(instance) == "http://example.com/?foo=bar"
	
	def test_path_usage(self):
		path = Path("/foo/bar/baz")
		instance = URI(path)
		assert instance.scheme == 'file'
		assert str(instance) == "file:///foo/bar/baz"


class TestURIDictlike(object):
	def test_get(self, instance):
		assert instance['name'] == 'ferret'
	
	def test_set_new(self, instance, empty):
		instance['foo'] = 'bar'
		assert str(instance) == 'http://user:pass@example.com/over/there?name=ferret&foo=bar#anchor'
		
		empty['bar'] = 'baz'
		assert str(empty) == 'http://example.com/over/there?bar=baz'
	
	def test_set_replace(self, instance):
		instance['name'] = 'lemur'
		assert str(instance) == 'http://user:pass@example.com/over/there?name=lemur#anchor'
	
	def test_del(self, instance):
		del instance['name']
		assert str(instance) == 'http://user:pass@example.com/over/there#anchor'
	
	def test_iter(self, instance):
		assert list(instance) == ["name=ferret"]
	
	def test_get_fail(self, instance, empty):
		with pytest.raises(KeyError):
			instance['foo']
		
		with pytest.raises(KeyError):
			empty['name']
	
	def test_repr(self, instance, empty):
		assert repr(instance) == "URI('http://user@example.com/over/there?name=ferret#anchor')"
		assert repr(empty) == "URI('http://example.com/over/there')"
