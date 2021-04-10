"""Web Platform Tests

These incorporate tests from a JSON file handed down through several projects.

https://github.com/web-platform-tests/wpt/blob/master/url/resources/urltestdata.json
http://trac.webkit.org/browser/trunk/LayoutTests/fast/url/script-tests/segments.js

The latter is no longer accessible.
"""

from json import load
from pathlib import PosixPath

import pytest

from uri import URI, Path

SENTINEL = object()

with open(PosixPath(__file__).parent / 'platform.json', 'rb') as fh:
	URI_COMPONENTS = []
	
	for r in load(fh):
		if isinstance(r, str): continue  # Skip comments.
		if r.get('failure'): continue  # Skip failure cases for now.
		if 'f:\n' in r['input']: continue  # Skip "breaking" whitespace tests for now.
		
		URI_COMPONENTS.append((
				r['input'],
				dict(
						base = r['base'],
						scheme = r['protocol'].rstrip(':'),  # ** We do not include : in the scheme.
						user = r['username'] or None,  # ** We use None instead of empty values.
						password = r['password'] or None,
						host = r['host'],
						port = int(r['port']) if r['port'] else None,  # ** Our port numbers are integer numeric.
						path = Path(r['pathname']),  # ** We use rich PurePosixPath objects.
						qs = r['search'].lstrip('?'),  # ** Our query string does not include its separator.
						fragment = r['hash'] if r['hash'] else None,
						relative = False,
					),
				r['href']
			))

for _uri, _parts, _expected in URI_COMPONENTS:
	_parts['uri'] = _uri
	if 'user' in _parts: _parts['username'] = _parts['user']
	if 'qs' in _parts: _parts['query'] = _parts['qs'].replace('%20', '+')  # We use compact + notation for spaces.
	if 'host' in _parts: _parts['hostname'] = _parts['host']
	if 'username' in _parts and _parts['username']:
		_parts['auth'] = _parts['username']
	if 'password' in _parts and _parts['password']:
		_parts.setdefault('auth', '')
		_parts['auth'] = _parts['auth'] + ':' + _parts['password']


@pytest.mark.parametrize('string,attributes,expected', URI_COMPONENTS)
class TestPlatform:
	@pytest.mark.parametrize('component', URI.__all_parts__ | {'base', 'qs', 'relative'})
	def test_component(self, string, attributes, expected, component):
		base = URI(attributes['base'])
		instance = base.resolve(string)
		
		assert str(instance) == expected
		
		#value = getattr(instance, component, SENTINEL)
		#
		#if component not in attributes:
		#	assert value in (None, SENTINEL, '')
		#	return
		#
		#assert value == attributes[component]
