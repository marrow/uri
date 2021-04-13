"""Functional and representative tests for the URI datatype/representation."""

from urllib.parse import urljoin, urlparse

import pytest

from uri import Path
from uri.qso import SENTINEL
from uri.uri import URI

URI_COMPONENTS = [
		# From test_deconstruct_url.py EXPECTED_DATA
		('http://site.com/', dict(  # ** for identity test to pass, must have path
				scheme = 'http',
				authority = 'site.com',
				heirarchical = 'site.com/',
				password = None,
				host = 'site.com',
				port = None,
				path = Path('/'),  # **
				relative = False,
				summary = 'site.com/',
				base = 'http://site.com/',
			)),
		('http://user@www.example.com:8080/path/index.html?param=val#fragment', dict(
				scheme = 'http',
				auth = 'user',
				authentication = 'user',
				authority = 'user@www.example.com:8080',
				heirarchical = 'user@www.example.com:8080/path/index.html',
				host = 'www.example.com',
				port = 8080,
				path = Path('/path/index.html'),  # **
				user = 'user',
				username = 'user',
				relative = False,
				summary = 'www.example.com/path/index.html',
				base = 'http://user@www.example.com:8080/path/index.html',
				query = 'param=val',
				qs = 'param=val',
				fragment = 'fragment',
			)),
		# From test_normalize_host.py
		('http://xn--e1afmkfd.xn--80akhbyknj4f/', dict(  # ** for identity test to pass, must provide encoded form
				scheme = 'http',
				authority = 'xn--e1afmkfd.xn--80akhbyknj4f',
				heirarchical = 'xn--e1afmkfd.xn--80akhbyknj4f/',
				password = None,
				host = 'пример.испытание',
				port = None,
				path = Path('/'),
				relative = False,
				summary = 'пример.испытание/',
				base = 'http://xn--e1afmkfd.xn--80akhbyknj4f/',
			)),
	]

for _uri, _parts in URI_COMPONENTS:
	_parts['uri'] = _uri
	if 'query' in _parts: _parts['qs'] = _parts['query']
	if 'host' in _parts: _parts['hostname'] = _parts['host']


def test_normalize_scheme():
	instance = URI('http://site.com/')
	assert instance.scheme == 'http'
	
	instance = URI('HTTP://site.com/')
	assert instance.scheme == 'http'


def test_normalize_host():
	instance = URI('http://SITE.COM/')
	assert instance.host == 'site.com'
	
	instance = URI('http://site.com./')
	assert instance.host == 'site.com'


@pytest.mark.parametrize('string,attributes', URI_COMPONENTS)
class TestURLNormalize:
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
	
	@pytest.mark.parametrize('component', URI.__all_parts__ | {'base', 'qs', 'summary', 'relative'})
	def test_component(self, string, attributes, component):
		instance = URI(string)
		value = getattr(instance, component, SENTINEL)
		
		if component not in attributes:
			assert value in (None, SENTINEL, '')
			return
		
		assert value == attributes[component]
