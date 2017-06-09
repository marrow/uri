# encoding: utf-8

from __future__ import unicode_literals

import pytest

from uri.compat import SENTINEL, str
from uri.qso import QSO, Bucket

EXAMPLES = [
		# Abstract
		('', (), {}),
		('foo=bar', (), {'foo': 'bar'}),
		
		# Multiple Arguments
		('foo&bar&baz&diz', ('foo', 'bar', 'baz', 'diz'), {}),
		
		# From Wikipedia - https://en.wikipedia.org/wiki/Query_string
		('name=ferret', (), {'name': 'ferret'}),
		('name=ferret&color=purple', (), {'name': 'ferret', 'color': 'purple'}),
		('field1=value1&field2=value2&field3=value3', (), {'field1': 'value1', 'field2': 'value2', 'field3': 'value3'}),
		('argument1+argument2+argument3', ('argument1 argument2 argument3', ), {}),
		
		# RFC 3986 (URI) - http://pretty-rfc.herokuapp.com/RFC3986
		('objectClass?one', ('objectClass?one', ), {}),
		('objectClass/one', ('objectClass/one', ), {}),
		
		#('', (), {}),
	]

MULTI_VALUE_EXAMPLES = [
		('key=value1&key=value2&key=value3', {'key': ['value1', 'value2', 'value3']}),
		('key=value1&foo=bar&key=value2', {'key': ['value1', 'value2']}),
		('key=value1&foo&key=value2&bar&key=value3', {'key': ['value1', 'value2', 'value3'], None: ['foo', 'bar']}),
		('foo&key=value1&foo=bar&key=value2&foo=baz&diz', {'key': ['value1', 'value2'], None: ['foo', 'diz'], 'foo': ['bar', 'baz']}),
		('foo=bar&key=value1&diz=foo&key=value2&foo=baz', {'foo': ['bar', 'baz'], 'key': ['value1', 'value2'], 'diz': 'foo'}),
		#('', {}),
	]

ASSIGNMENT_EXAMPLES = [
		('key=value1&key=value2', 0, 'value3', 'key=value3&key=value2'),
		('key=value1&key=value2', 1, 'value3', 'key=value1&key=value3'),
		('key=value1&key=value2', 0, ('foo', 'value'), 'foo=value&key=value2'),
		('key=value1&key=value2', 1, ('foo', 'value'), 'key=value1&foo=value'),
		('key=value1&key=value2', 'key', ('foo', 'value'), 'foo=value'),
		('bar=baz&key=value1&key=value2', 'key', ('foo', 'value'), 'bar=baz&foo=value'),
		('key=value1&bar=baz&key=value2', 'key', ('foo', 'value'), 'bar=baz&foo=value'),
		('key=value1&key=value2&bar=baz', 'key', ('foo', 'value'), 'bar=baz&foo=value'),
		('bar=baz&key=value1&key=value2', 1, ('foo', 'value'), 'bar=baz&foo=value&key=value2'),
		('key=value1&bar=baz&key=value2', 0, ('foo', 'value'), 'foo=value&bar=baz&key=value2'),
		('key=value1&bar=baz&key=value2', 2, ('foo', 'value'), 'key=value1&bar=baz&foo=value'),
		('key=value1&key=value2&bar=baz', 0, ('foo', 'value'), 'foo=value&key=value2&bar=baz'),
		('key=value1&key=value2&bar=baz', 1, ('foo', 'value'), 'key=value1&foo=value&bar=baz'),
		('key=value1&key=value2&bar=baz', 2, ('foo', 'value'), 'key=value1&key=value2&foo=value'),
		#('', , '', ''),
	]

DELETION_EXAMPLES = [
		('key=value1&key=value2&bar=baz', 0, 'key=value2&bar=baz', ['key', 'value1']),
		('key=value1&key=value2&bar=baz', 1, 'key=value1&bar=baz', ['key', 'value2']),
		('key=value1&key=value2&bar=baz', 2, 'key=value1&key=value2', ['bar', 'baz']),
		('key=value1&key=value2&bar=baz', 'key', 'bar=baz', [Bucket('key', 'value1'), Bucket('key', 'value2')]),
		('key=value1&key=value2&bar=baz', 'bar', 'key=value1&key=value2', ['bar', 'baz']),
		('key=value1&bar=baz&key=value2', 'bar', 'key=value1&key=value2', ['bar', 'baz']),
		#('', , ''),
	]

POP_EXAMPLES = [
		('key=value1&key=value2&bar=baz', 0, 'key=value2&bar=baz', Bucket('key', 'value1')),
		('key=value1&key=value2&bar=baz', 1, 'key=value1&bar=baz', Bucket('key', 'value2')),
		('key=value1&key=value2&bar=baz', 2, 'key=value1&key=value2', Bucket('bar', 'baz')),
		('key=value1&key=value2&bar=baz', 'key', 'key=value1&bar=baz', 'value2'),
		('key=value1&key=value2&bar=baz', 'bar', 'key=value1&key=value2', 'baz'),
		('key=value1&bar=baz&key=value2', 'bar', 'key=value1&key=value2', 'baz'),
		('key=value1&bar=baz&key=value2', SENTINEL, 'key=value1&bar=baz', Bucket('key', 'value2')),
		#('', , ''),
	]

UPDATE_EXAMPLES = [
		('key=value1&key=value2&bar=baz', 'foo=bar', 'key=value1&key=value2&bar=baz&foo=bar'),
		('key=value1&key=value2&bar=baz', 'key=value3', 'bar=baz&key=value3'),
		('key=value1&key=value2&bar=baz', 'bar=diz', 'key=value1&key=value2&bar=diz'),
		('key=value1&key=value2&bar=baz', dict(foo='bar'), 'key=value1&key=value2&bar=baz&foo=bar'),
		('key=value1&key=value2&bar=baz', ('foo=bar', 'baz=diz'), 'key=value1&key=value2&bar=baz&foo=bar&baz=diz'),
		('key=value1&key=value2&bar=baz', Bucket('foo', 'bar'), 'key=value1&key=value2&bar=baz&foo=bar'),
		('key=value1&key=value2&bar=baz', QSO("foo=baz&bar=diz"), 'key=value1&key=value2&bar=diz&foo=baz'),
	]

COMBINATION_EXAMPLES = [
		('key=value1&key=value2&bar=baz', 'foo=bar', 'key=value1&key=value2&bar=baz&foo=bar'),
		('key=value1&key=value2&bar=baz', 'key=value3', 'key=value1&key=value2&bar=baz&key=value3'),
		('key=value1&key=value2&bar=baz', 'bar=diz', 'key=value1&key=value2&bar=baz&bar=diz'),
		('key=value1&key=value2&bar=baz', dict(foo='bar'), 'key=value1&key=value2&bar=baz&foo=bar'),
		('key=value1&key=value2&bar=baz', ('foo=bar', ), 'key=value1&key=value2&bar=baz&foo=bar'),
		('key=value1&key=value2&bar=baz', Bucket('foo', 'bar'), 'key=value1&key=value2&bar=baz&foo=bar'),
		('key=value1&key=value2&bar=baz', QSO("foo=baz&bar=diz"), 'key=value1&key=value2&bar=baz&foo=baz&bar=diz'),
	]

COMPARISON_EXAMPLES = [
		('', ''),
		('key=value1&key=value2&bar=baz', QSO('key=value1&key=value2&bar=baz')),
	]


class TestQSO(object):
	@pytest.mark.parametrize('string,values', MULTI_VALUE_EXAMPLES)
	def test_multiple_values(self, string, values):
		instance = QSO(string)
		
		for key in values:
			if not isinstance(values[key], list): continue
			result = list(instance[key])
			assert result == values[key]
	
	@pytest.mark.parametrize('src,key,value,expect', ASSIGNMENT_EXAMPLES)
	def test_multiple_reassignment(self, src, key, value, expect):
		instance = QSO(src)
		instance[key] = value
		assert str(instance) == expect
	
	def test_numeric_deletion(self):
		instance = QSO('key=value1&key=value2&bar=baz')
		assert len(instance) == 3
		assert len(instance.groups['key']) == 2
		del instance[0]
		assert len(instance) == 2
		assert len(instance.groups['key']) == 1
		assert str(instance) == 'key=value2&bar=baz'
	
	@pytest.mark.parametrize('src,key,expect,value', DELETION_EXAMPLES)
	def test_deletion_examples(self, src, key, expect, value):
		instance = QSO(src)
		del instance[key]
		assert str(instance) == expect
	
	@pytest.mark.parametrize('src,change,expect', UPDATE_EXAMPLES)
	def test_update(self, src, change, expect):
		instance = QSO(src)
		instance.update(change)
		assert str(instance) == expect
	
	def test_update_keywords(self):
		instance = QSO("key=value1&key=value2&bar=baz")
		instance.update(bar="diz")
		assert str(instance) == "key=value1&key=value2&bar=diz"
		instance.update(diz="doz")
		assert str(instance) == "key=value1&key=value2&bar=diz&diz=doz"
		instance.update(key="value3")
		assert str(instance) == "bar=diz&diz=doz&key=value3"
	
	@pytest.mark.parametrize('src,change,expect', COMBINATION_EXAMPLES)
	def test_inline_add(self, src, change, expect):
		instance = QSO(src)
		instance += change
		assert str(instance) == expect
	
	def test_index(self):
		instance = QSO("foo=bar&baz=diz")
		assert instance.index('foo=bar') == 0
		assert instance.index('baz=diz') == 1
		
		with pytest.raises(ValueError):
			instance.index('diz')
	
	def test_count(self):
		instance = QSO("")
		assert instance.count('foo') == 0
		
		instance = QSO("foo&bar=value1&baz=diz&bar=value2")
		assert instance.count('foo') == 1
		assert instance.count('bar') == 2
		assert instance.count('baz') == 1
	
	def test_insert(self):
		instance = QSO("foo&bar&baz")
		instance.insert(0, "diz")
		assert str(instance) == "diz&foo&bar&baz"
		instance.insert(-1, "doz")
		assert str(instance) == "diz&foo&bar&doz&baz"
		assert len(instance.groups[None]) == 5
		instance.insert(99, "twentyseven")
		assert str(instance) == "diz&foo&bar&doz&baz&twentyseven"
	
	@pytest.mark.parametrize('src,value', COMPARISON_EXAMPLES)
	def test_comparison(self, src, value):
		instance = QSO(src)
		assert instance == value
		assert not (instance != value)
	
	@pytest.mark.parametrize('src,key,expect,value', POP_EXAMPLES)
	def test_pop_examples(self, src, key, expect, value):
		instance = QSO(src)
		result = instance.pop(key)
		assert str(instance) == expect
		assert result == value
	
	@pytest.mark.parametrize('key', ['baz', 2, SENTINEL])
	def test_pop_failures(self, key):
		instance = QSO()
		
		with pytest.raises(KeyError):
			instance.pop(key)
	
	def test_pop_defaults(self):
		instance = QSO()
		
		assert instance.pop(default=None) is None
		assert instance.pop(0, None) is None
		assert instance.pop('named', None) is None
	
	def test_pop_failure(self):
		instance = QSO()
		
		with pytest.raises(KeyError):
			instance.pop('key')
	
	def test_reverse(self):
		instance = QSO("key=value1&key=value2&bar=baz")
		instance.reverse()
		assert str(instance) == "bar=baz&key=value2&key=value1"
		assert tuple(instance['key']) == ("value2", "value1")
	
	def test_keys(self):
		instance = QSO("key=value1&key=value2&bar=baz")
		assert tuple(instance.keys()) == ('key', 'key', 'bar')
	
	def test_items(self):
		instance = QSO("key=value1&key=value2&bar=baz")
		assert tuple(instance.items()) == (('key', 'value1'), ('key', 'value2'), ('bar', 'baz'))
	
	def test_values(self):
		instance = QSO("key=value1&key=value2&bar=baz")
		assert tuple(instance.values()) == ('value1', 'value2', 'baz')
	
	def test_get(self):
		instance = QSO("key=value1&key=value2&bar=baz")
		assert tuple(instance.get('key')) == ('value1', 'value2')
		assert instance.get('bar') == 'baz'
		assert instance.get('baz') is None
	
	def test_clear(self):
		instance = QSO("key=value1&key=value2&bar=baz")
		assert len(instance) == 3
		instance.clear()
		assert len(instance) == 0
		assert not instance
		assert not instance.groups


@pytest.mark.parametrize('string,args,kw', EXAMPLES)
class TestQSOExamples(object):
	def test_repr(self, string, args, kw):
		instance = QSO(string)
		assert repr(instance) == 'QSO("' + string + '")'
	
	def test_str(self, string, args, kw):
		instance = QSO(string)
		assert str(instance) == string
	
	def test_length(self, string, args, kw):
		instance = QSO(string)
		
		if len(instance) != (len(args) + len(kw)):
			__import__('pudb').set_trace()
			instance = QSO(string)
		
		assert len(instance) == (len(args) + len(kw))
	
	def test_contains(self, string, args, kw):
		instance = QSO(string)
		
		for i in range(len(args) + len(kw)):
			assert i in instance
	
	def test_named_assignment(self, string, args, kw):
		instance = QSO(string)
		instance['doz'] = '27'
		
		assert str(instance).endswith(('&' if (args or kw) else '') + 'doz=27')


@pytest.mark.parametrize('string,args,kw', [i for i in EXAMPLES if i[1]])
class TestQSOPositionalUse(object):
	def test_iteration_view(self, string, args, kw):
		instance = QSO(string)
		
		for bucket, arg in zip(instance, args):
			assert bucket.value == arg


@pytest.mark.parametrize('string,args,kw', [i for i in EXAMPLES if i[2]])
class TestQSOKeywordUse(object):
	def test_contains(self, string, args, kw):
		instance = QSO(string)
		
		for key in kw:
			assert key in instance
	
	def test_grouped_indexing(self, string, args, kw):
		instance = QSO(string)
		
		for key, value in kw.items():
			assert instance[key] == value
	
	def test_grouped_replacement(self, string, args, kw):
		instance = QSO(string)
		
		instance['foo'] = 'doz'
		
		assert 'foo=doz' in str(instance)


@pytest.mark.parametrize('string,args,kw', [i for i in EXAMPLES if len(i[1]) > 1])
class TestQSOMultiplePositional(object):
	def test_reversing(self, string, args, kw):
		instance = QSO(string)
		result = list(reversed(instance))
		
		assert len(result) == len(args)
		assert tuple(i.value for i in result) == args[::-1]
	
	def test_numeric_indexing(self, string, args, kw):
		instance = QSO(string)
		
		for i, arg in enumerate(args):
			assert instance[i] == arg
	
	def test_indexed_replacement(self, string, args, kw):
		instance = QSO(string)
		instance[1] = 'doz'
		assert '&doz'
