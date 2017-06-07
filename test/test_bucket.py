# encoding: utf-8

from __future__ import unicode_literals

import pytest

from uri.bucket import Bucket
from uri.compat import str

EXAMPLES = [
		# String,       Arguments,         Name,    Value,      Valid
		
		( '',           ('', ),            None,    '',         True ),
		( 'foo',        ('foo', ),         None,    'foo',      True ),
		( 'foo',        (None, 'foo'),     None,    'foo',      True ),
		( 'foo=bar',    ('foo', 'bar'),    'foo',   'bar',      True ),
		
		( '=foo=bar',   ('=foo=bar', ),    '',      'foo=bar',   False ),
		( '=foo=bar',   ('=foo', 'bar'),   '=foo',  'bar',       False ),
		( '=foo=bar',   ('', 'foo=bar'),   '',      'foo=bar',   False ),
		( 'foo=bar=',   ('foo', 'bar='),   'foo',   'bar=',      False ),
		( 'foo==bar=',  ('foo=', 'bar='),  'foo=',  'bar=',      False ),
		( 'foo==bar=',  ('foo==bar=', ),   'foo',   '=bar=',     False ),
		( '=foo=bar=',  ('=foo=bar=', ),   '',      'foo=bar=',  False ),
		
	]


@pytest.mark.parametrize('string,args,name,value,valid', EXAMPLES)
class TestBucketExamples(object):
	def test_string_identity(self, string, args, name, value, valid):
		bucket = Bucket(string)
		assert str(bucket) == string
	
	def test_names(self, string, args, name, value, valid):
		bucket = Bucket(*args)
		assert bucket.name == name
	
	def test_values(self, string, args, name, value, valid):
		bucket = Bucket(*args)
		assert bucket.value == value
	
	def test_validity(self, string, args, name, value, valid):
		bucket = Bucket(string)
		assert bucket.valid == valid
	
	def test_identity_comparison(self, string, args, name, value, valid):
		bucket = Bucket(string)
		assert bucket == string
	
	def test_unequal_comparison(self, string, args, name, value, valid):
		bucket = Bucket(*args)
		assert not (bucket == "xxx")
	
	def test_not_equal_comparison(self, string, args, name, value, valid):
		bucket = Bucket(*args)
		assert bucket != "xxx"
	
	def test_repr(self, string, args, name, value, valid):
		bucket = Bucket(*args)
		assert repr(bucket) == "Bucket(" + str(bucket) + ")"
	
	def test_length(self, string, args, name, value, valid):
		bucket = Bucket(*args)
		expected = 2 if '=' in string else 1
		assert len(bucket) == expected


@pytest.mark.parametrize('string,args,name,value,valid', [i for i in EXAMPLES if not i[4]])
class TestBucketExamplesInvalid(object):
	def test_strict_string_failure(self, string, args, name, value, valid):
		with pytest.raises(ValueError):
			Bucket(string, strict=True)
