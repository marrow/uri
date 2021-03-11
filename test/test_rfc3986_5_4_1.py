# encoding: utf-8

"""Tests representative of examples provided within the URI RFC 3986."""

from __future__ import unicode_literals

import pytest

from uri.compat import str
from uri.uri import URI


class ReferenceResolutionExample(object):
	"""As defined by the preface of section 5.4, these examples utilize a defined base URI.
	
	Reference: https://pretty-rfc.herokuapp.com/RFC3986#reference-examples
	"""
	
	BASE = URI("http://a/b/c/d;p?q")


class TestNormalExamples(ReferenceResolutionExample):
	"""Examples provided by section 5.4.1 of RFC 3986."""
	
	EXAMPLES = {
			"g:h": "g:h",
			"g": "http://a/b/c/g",
			"./g": "http://a/b/c/g",
			"g/": "http://a/b/c/g/",
			"/g": "http://a/g",
			# "//g": "http://g",  # This commented out case is the "correct" one.
			"//g": "http://g/",  # We force URL with authorities to have paths.
			"?y": "http://a/b/c/d;p?y",
			"g?y": "http://a/b/c/g?y",
			"#s": "http://a/b/c/d;p?q#s",
			"g#s": "http://a/b/c/g#s",
			"g?y#s": "http://a/b/c/g?y#s",
			";x": "http://a/b/c/;x",
			"g;x": "http://a/b/c/g;x",
			"g;x?y#s": "http://a/b/c/g;x?y#s",
			"": "http://a/b/c/d;p?q",
			".": "http://a/b/c/",
			"./": "http://a/b/c/",
			"..": "http://a/b/",
			"../": "http://a/b/",
			"../g": "http://a/b/g",
			"../..": "http://a/",
			"../../": "http://a/",
			"../../g": "http://a/g"
		}
	
	@pytest.mark.parametrize('href,result', EXAMPLES.items())
	def test_resolution_equivalence(self, href, result):
		resolved = self.BASE.resolve(href)
		assert str(resolved) == result


class TestAbnormalExamples(ReferenceResolutionExample):
	"""Examples provided by section 5.4.2 of RFC 3986."""
	
	EXAMPLES = {
			"../../../g": "http://a/g",
			"../../../../g": "http://a/g",
			
			"/./g": "http://a/g",
			"/../g": "http://a/g",
			"g.": "http://a/b/c/g.",
			".g": "http://a/b/c/.g",
			"g..": "http://a/b/c/g..",
			"..g": "http://a/b/c/..g",
			
			"./../g": "http://a/b/g",
			"./g/.": "http://a/b/c/g/",
			"g/./h": "http://a/b/c/g/h",
			"g/../h": "http://a/b/c/h",
			"g;x=1/./y": "http://a/b/c/g;x=1/y",
			"g;x=1/../y": "http://a/b/c/y",
			
			"g?y/./x": "http://a/b/c/g?y/./x",
			"g?y/../x": "http://a/b/c/g?y/../x",
			"g#s/./x": "http://a/b/c/g#s/./x",
			"g#s/../x": "http://a/b/c/g#s/../x",
			
			# "http:g": "http:g", # for strict parsers
			"http:g": "http://a/b/c/g", # for backward compatibility
		}
	
	@pytest.mark.parametrize('href,result', EXAMPLES.items())
	def test_resolution_equivalence(self, href, result):
		resolved = self.BASE.resolve(href)
		assert str(resolved) == result

