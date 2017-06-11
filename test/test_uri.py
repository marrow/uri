# encoding: utf-8

from __future__ import unicode_literals

from uri.uri import URI


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
