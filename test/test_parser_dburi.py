import pytest

from uri import URI
from uri.parse.db import parse_dburi
from uri.qso import SENTINEL

EXAMPLES = {
		# Examples from: https://github.com/ferrix/dj-mongohq-url/blob/master/test_dj_mongohq_url.py
		'': {
				'name': '',
				'host': None,
				'user': None,
				'password': None,
				'port': None
			},
		'mongodb://heroku:wegauwhgeuioweg@linus.mongohq.com:10031/app4523234': {
				'engine': 'mongodb',
				'name': 'app4523234',
				'host': 'linus.mongohq.com',
				'user': 'heroku',
				'password': 'wegauwhgeuioweg',
				'port': 10031
			},
		'postgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn': {
				'engine': 'postgis',
				'name': 'd8r82722r2kuvn',
				'host': 'ec2-107-21-253-135.compute-1.amazonaws.com',
				'user': 'uf07k1i6d8ia0v',
				'password': 'wegauwhgeuioweg',
				'port': 5431
			},
		
	#	'': {
	#			'engine': '',
	#			'name': ''
	#			'host': ''
	#			'user': ''
	#			'password': ''
	#			'port': 
	#		},
	}


@pytest.mark.parametrize('string,attributes', EXAMPLES.items())
class TestDBURIParsing:
	@pytest.mark.parametrize('component', URI.__all_parts__ | {'base', 'qs', 'summary', 'relative'})
	def test_component(self, string, attributes, component):
		return
		
		instance = URI(string)
		value = getattr(instance, component, SENTINEL)
		
		if component not in attributes:
			assert value in (None, SENTINEL, '')
			return
		
		assert value == attributes[component]
