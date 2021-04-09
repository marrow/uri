"""Functional and representative tests for the URI datatype/representation."""

from urllib.parse import urljoin, urlparse

import pytest

from uri import Path
from uri.qso import SENTINEL
from uri.uri import URI

URI_COMPONENTS = [
		# From test_url.py
		('http://www.google.com:443/', dict(  # test_url_scheme ** Changing scheme does not alter port.
				scheme = 'http',  # ** We do not "correct" this, either.
				authority = 'www.google.com:443',
				heirarchical = 'www.google.com:443/',
				password = None,
				host = 'www.google.com',
				hostname = 'www.google.com',
				port = 443,
				path = Path('/'),  # **
				relative = False,
				summary = 'www.google.com/',
				base = 'http://www.google.com:443/',
			)),
		('https://www.google.com/', dict(  # test_url_host **
				scheme = 'https',
				authority = 'www.google.com',
				heirarchical = 'www.google.com/',
				host = 'www.google.com',
				hostname = 'www.google.com',
				path = Path('/'),  # **
				relative = False,
				summary = 'www.google.com/',
				base = 'https://www.google.com/',
			)),
		
		# From test_special_cases.py
		('http://1.1.1.1 &@2.2.2.2/# @3.3.3.3', dict(  # test_spaces_with_multiple_ipv4_addresses **
				scheme = 'http',
				authority = '1.1.1.1 &@2.2.2.2',  # **
				heirarchical = '1.1.1.1 &@2.2.2.2/',
				auth = '1.1.1.1 &',  # **
				authentication = '1.1.1.1 &',  # **
				user = '1.1.1.1 &',  # **
				username = '1.1.1.1 &',  # **
				host = '2.2.2.2',
				fragment = ' @3.3.3.3',
				path = Path('/'),
				relative = False,
				summary = '2.2.2.2/',
				base = 'http://1.1.1.1 &@2.2.2.2/',
			)),
		('http://google.com/#@evil.com/', dict(  # test_fragment_with_hostname **
				scheme = 'http',
				authority = 'google.com',
				heirarchical = 'google.com/',
				host = 'google.com',
				path = Path('/'),
				fragment = '@evil.com/',
				relative = False,
				base = 'http://google.com/',
				summary = 'google.com/',
			)),
		('http://foo@evil.com:80@google.com/', dict(  # test_multiple_ats_within_authority
				scheme = 'http',
				authority = 'foo@evil.com:80@google.com',
				auth = 'foo@evil.com:80',
				heirarchical = 'foo@evil.com:80@google.com/',
				host = 'google.com',
				user = 'foo@evil.com',  # **
				password = '80',
				path = Path('/'),
				summary = 'google.com/',
				authentication = 'foo@evil.com:80',
				relative = False,
				base = 'http://foo@evil.com:80@google.com/',
				username = 'foo@evil.com',
			)),
		('http://foo@evil.com:80 @google.com/', dict(  # test_multiple_ats_and_space_within_authority **
				scheme = 'http',
				authority = 'foo@evil.com:80 @google.com',
				authentication = 'foo@evil.com:80 ',
				heirarchical = 'foo@evil.com:80 @google.com/',
				host = 'google.com',
				user = 'foo@evil.com',  # **
				username = 'foo@evil.com',  # **
				password = '80 ',  # **
				path = Path('/'),
				auth = 'foo@evil.com:80 ',
				relative = False,
				summary = 'google.com/',
				base = 'http://foo@evil.com:80 @google.com/',
			)),
		('http://orange.tw/sandbox/ＮＮ/passwd', dict(  # test_unicode_double_dot_if_stripped_bom
				scheme = 'http',
				authority = 'orange.tw',
				heirarchical = 'orange.tw/sandbox/ＮＮ/passwd',
				host = 'orange.tw',
				path = Path('/sandbox/ＮＮ/passwd'),  # **
				relative = False,
				summary = 'orange.tw/sandbox/ＮＮ/passwd',
				base = 'http://orange.tw/sandbox/ＮＮ/passwd',
			)),
		('http://127.0.0.1\tfoo.google.com/', dict(  # test_host_contains_tab_in_authority **
				scheme = 'http',
				authority = '127.0.0.1\tfoo.google.com',
				heirarchical = '127.0.0.1\tfoo.google.com/',
				host = '127.0.0.1\tfoo.google.com',  # **
				path = Path('/'),
				relative = False,
				base = 'http://127.0.0.1\tfoo.google.com/',
				summary = '127.0.0.1\tfoo.google.com/',
			)),
		# Omitted: test_host_contains_tab_in_authority_single_or_double_encoded, test_injection_within_authority
		('http://localhost\\@google.com:12345/', dict(  # test_backslash_within_authority **
				scheme = 'http',
				authority = 'localhost\\@google.com:12345',
				auth = 'localhost\\',
				authentication = 'localhost\\',
				heirarchical = 'localhost\\@google.com:12345/',
				user = 'localhost\\',
				username = 'localhost\\',
				host = 'google.com',  # **
				port = 12345,
				path = Path('/'),  # **
				relative = False,
				base = 'http://localhost\\@google.com:12345/',
				summary = 'google.com/',
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
class TestWhatwgURI:
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


class TestWhatwgURL:
	def test_url_scheme(self):
		url = URI('http://www.google.com:443/')  # **
		url.scheme = 'https'
		
		assert url.scheme == 'https'
		assert url.port == 443  # ** Whatwg-URL clears port on scheme changes. Unsure why. Only if default?
		assert str(url) == 'https://www.google.com:443/'  # ** We do not elide default port numbers.
	
	def test_url_host(self):
		url = URI("https://www.google.com")
		url.hostname = "example.com"
		
		assert url.hostname == "example.com"
		assert str(url) == "https://example.com/"
	
	def test_url_port(self):
		url = URI("https://www.example.com")
		url.port = 123
		
		assert url.port == 123
		assert url.host == "www.example.com"  # ** We do not include port number in host name.
		assert url.authority == "www.example.com:123"  # It is includes in the authority, however.
		assert str(url) == "https://www.example.com:123/"
		
		url.port = 443
		
		assert url.port == 443  # ** Similarly, we don't treat default assignments as None assignments.
		assert url.host == "www.example.com"
		assert str(url) == "https://www.example.com:443/"  # **
	
	def test_relative_url_with_url_contained(self, instance):
		url = URI('https://www.google.com').resolve('/redirect?target=http://localhost:61020/')
		
		assert url.scheme == 'https'
		assert url.host == 'www.google.com'
		assert url.path == Path('/redirect')
		assert str(url.query) == "target=http%3A//localhost%3A61020/"  # ** We automatically encode and correct.
	
	def test_url_user_info(self):
		url = URI("https://github.com")
		url.user = "username"
		
		assert url.username == "username"
		assert url.password is None
		assert str(url) == "https://username@github.com/"
		
		url.password = "password"
		
		assert url.username == "username"
		assert url.password == "password"
		assert str(url) == "https://username:password@github.com/"
		
		url.username = None
		
		assert url.username is None
		assert url.password == "password"
		assert str(url) == "https://:password@github.com/"
		
		url.password = None
		
		assert url.username is None
		assert url.password is None
		assert str(url) == "https://github.com/"
	
	def test_url_query(self):
		url = URI("https://www.google.com")
		url.query = "a=1"  # ** Don't include the prefix yourself.
		
		assert url.qs == "a=1"
		assert str(url) == "https://www.google.com/?a=1"
		
		url.query = ""
		
		assert url.query == ""
		assert str(url) == "https://www.google.com/"  # ** If empty or None, we do not emit the separator.
		
		url.query = None
		
		assert not url.query  # ** It isn't literally None, but it is falsy if omitted or empty.
		assert str(url) == "https://www.google.com/"
		# The above is due to the fact that `.query` returns a rich, dict-like object which permits mutation.
		# Assigning None just clears this mutable structure.
	
	def test_url_fragment(self):
		url = URI("https://www.google.com")
		url.fragment = "abc"
		
		assert url.fragment == "abc"
		assert str(url) == "https://www.google.com/#abc"
		
		url.fragment = ""
		
		assert url.fragment == ""
		assert str(url) == "https://www.google.com/"  # ** None and an empty string are both interpreted as "none".
		
		url.fragment = None
		
		assert url.fragment is None
		assert str(url) == "https://www.google.com/"
	
	def test_url_origin(self):  # ** Not _entirely_ the same, as the components come back recombined, not as a tuple.
		url = URI("https://www.google.com")
		assert url.origin == "https://www.google.com"
	
	@pytest.mark.xfail(reason="Need to look into definition of 'origin' for URI generally.")
	def test_url_blob_origin(self):
		url = URI("blob:https://www.google.com")
		
		assert url.origin == URI("https://www.google.com").origin


@pytest.mark.parametrize('url', [
		"https://www.google.com/",
		"http://user:pass@www.example.com/",
		"http://:pass@www.example.com/",
		"http://user@www.example.com/",
		"http://www.example.com:432/",
		"http://www.example.com/?a=1;B=c",
		"http://www.example.com/#Fragment",
		"http://username:password@www.example.com:1234/?query=string#fragment",
	])
@pytest.mark.parametrize('attr', ['netloc', 'hostname', 'port', 'path', 'query', 'fragment', 'username', 'password'])
def test_assert_same_urlparse_result(url, attr):
	urllib = urlparse(url)
	uri = URI(url)
	
	urllib_value = getattr(urllib, attr)
	uri_value = getattr(uri, attr)
	
	if urllib_value == "" and uri_value is None:
		pytest.xfail("URI uses None where urllib uses empty strings")
	
	elif isinstance(uri_value, Path):
		assert urllib_value == str(uri_value)  # First, ensure the string versions are equal...
		pytest.xfail("URI uses rich Path objects where urllib uses strings, which compared OK")
	
	assert urllib_value == uri_value


@pytest.mark.parametrize(('base', 'href', 'expected'), [
		("http://www.google.com/", "", "http://www.google.com/"),
		("http://www.google.com/", "/", "http://www.google.com/"),
		("http://www.google.com/", "maps/", "http://www.google.com/maps/"),
		("http://www.google.com/", "one/two/", "http://www.google.com/one/two/"),
		("http://www.google.com/mail", "/maps/", "http://www.google.com/maps/"),
		("http://www.google.com/", "./", "http://www.google.com/"),
		("http://www.google.com/maps", "..", "http://www.google.com/"),
		("http://www.google.com/", "https://www.google.com/", "https://www.google.com/"),
		("http://www.google.com/", "https://maps.google.com/", "https://maps.google.com/"),
		("https://www.google.com/", "https://www.google.com:1234/", "https://www.google.com:1234/"),
		("https://www.google.com/", "?query=string", "https://www.google.com/?query=string"),
		("https://www.google.com/", "#fragment", "https://www.google.com/#fragment"),
		("http://www.google.com/", "http://user:pass@www.google.com/", "http://user:pass@www.google.com/"),
		("http://www.google.com/", "http://user@www.google.com/", "http://user@www.google.com/"),
		("http://www.google.com/", "http://:pass@www.google.com/", "http://:pass@www.google.com/"),
	])
def test_assert_same_urljoin_result(base, href, expected):
	urllib = urljoin(base, href)
	uri_resolve = URI(base).resolve(href)
	uri_division = str(URI(base) / href)
	
	assert urllib == uri_resolve == uri_division == expected
