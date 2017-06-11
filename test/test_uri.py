# encoding: utf-8

from __future__ import unicode_literals

import pytest

from uri.compat import Path
from uri.uri import URI


def test_uri_wtf():
	with pytest.raises(TypeError):
		URI(foo="bar")


def test_basic_uri():
	https = URI("https://")
	instance = URI("http://user:pass@example.com/over/there?name=ferret#anchor")
	
	assert https.relative
	assert not instance.relative
	
	# Scalar URI components.
	assert instance.scheme == 'http'
	assert instance.user == 'user'
	assert instance.password == 'pass'
	assert instance.host == 'example.com'
	assert instance.query == 'name=ferret'
	assert instance.qs == 'name=ferret'
	
	# Compound URI components.
	assert instance.auth == 'user:pass'
	assert instance.authority == 'user:pass@example.com'
	assert instance.heirarchical == 'user:pass@example.com/over/there'
	assert instance.base == 'http://user:pass@example.com/over/there'
	assert instance.summary == 'example.com/over/there'
	
	# URI rendering.
	assert str(instance) == "http://user:pass@example.com/over/there?name=ferret#anchor"
	assert instance.uri == "http://user:pass@example.com/over/there?name=ferret#anchor"
	
	# Path-like manipulation.
	instance = https // instance
	assert str(instance) == "https://user:pass@example.com/over/there?name=ferret#anchor"
	
	instance = instance / "/foo"
	assert str(instance) == "https://user:pass@example.com/foo"
	
	instance /= "bar"
	assert str(instance) == "https://user:pass@example.com/foo/bar"
	
	assert str(instance.resolve('/baz')) == "https://user:pass@example.com/baz"
	assert str(instance.resolve('baz')) == "https://user:pass@example.com/foo/baz"


def test_qs_assignment():
	instance = URI("http://example.com")
	assert str(instance) == "http://example.com/"
	
	instance.qs = "foo=bar"
	assert str(instance) == "http://example.com/?foo=bar"


def test_path_usage():
	path = Path("/foo/bar/baz")
	instance = URI(path)
	assert instance.scheme == 'file'
	assert str(instance) == "file:///foo/bar/baz"
