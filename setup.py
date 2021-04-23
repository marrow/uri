#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import codecs

try:
	from setuptools.core import setup, find_packages
except ImportError:
	from setuptools import setup, find_packages


if sys.version_info < (3, 8):
	raise SystemExit("Python 3.8 or later is required.")

version = description = url = author = version_info = ''  # Actually loaded on the next line; be quiet, linter.
exec(open(os.path.join("uri", "release.py")).read())

here = os.path.abspath(os.path.dirname(__file__))

tests_require = [
		'pytest',  # test collector and extensible runner
		'pytest-cov',  # coverage reporting
		'pytest-flakes',  # syntax validation
		'pytest-isort',  # import ordering
		'webob',  # request WSGI environment mocking
		'markupsafe',  # bless use with a common HTML entity encoder and its encoding protocol
	]

trove_map = {
		'plan': "Development Status :: 1 - Planning",
		'alpha': "Development Status :: 3 - Alpha",
		'beta': "Development Status :: 4 - Beta",
		'final': "Development Status :: 5 - Production/Stable",
	}


# # Entry Point

setup(
	name = "uri",
	version = version,
	description = description,
	long_description = codecs.open(os.path.join(here, 'README.rst'), 'r', 'utf8').read(),
	url = url,
	author = author.name,
	author_email = author.email,
	license = 'MIT',
	keywords = ['type', 'URI', 'URL', 'rfc', 'rfc'],
	classifiers = [
			trove_map[version_info.releaselevel],
			"Intended Audience :: Developers",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			"Programming Language :: Python",
			"Programming Language :: Python :: 3",
			"Programming Language :: Python :: 3.8",
			"Programming Language :: Python :: 3.9",
			"Programming Language :: Python :: Implementation :: CPython",
			"Programming Language :: Python :: Implementation :: PyPy",
			"Topic :: Software Development :: Libraries :: Python Modules",
			"Topic :: Utilities"
		],
	
	packages = find_packages(exclude=['test', 'htmlcov']),
	include_package_data = True,
	package_data = {'': ['README.rst', 'LICENSE.txt']},
	zip_safe = False,
	
	# ## Dependency Declaration
	python_requires = ">=3.8",
	
	setup_requires = [
			'pytest-runner',
		] if {'pytest', 'test', 'ptr'}.intersection(sys.argv) else [],
	
	install_requires = [],  # URI has no runtime dependencies.
	
	extras_require = dict(
			http = ['requests'],  # Support for the http:// and https:// protocols.
			development = tests_require + [  # Development-time dependencies.
					'pre-commit',  # Commit hooks for code quality.
					'mypy',  # Type hinting analysis.
					'rope',  # Project symbols collection.
					'bandit',  # Automated security analysis.
					'ptipython',  # Enhanced interactive REPL shell.
					'e',  # python -me
				],
		),
	
	tests_require = tests_require,
	
	# ## Plugin Registration
	
	entry_points = {
				'uri.scheme': [
						# https://www.iana.org/assignments/uri-schemes/uri-schemes.xhtml
						# https://www.w3.org/wiki/UriSchemes
						'file = uri.scheme:URLScheme',
						'ftp = uri.scheme:URLScheme',
						'http = uri.scheme:URLScheme',
						'https = uri.scheme:URLScheme',
						'irc = uri.scheme:URLScheme',
						'ldap = uri.scheme:URLScheme',
						'telnet = uri.scheme:URLScheme',
						'sftp = uri.scheme:URLScheme',
						# Care of https://github.com/APSL/uri/commit/709b4b73daae7b8651b92fd4fa63af41c4db2986
						'mysql = uri.scheme:URLScheme',
						'redis = uri.scheme:URLScheme',
						# https://docs.mongodb.com/manual/reference/connection-string
						'mongodb = uri.scheme:URLScheme',
						# https://en.wikipedia.org/wiki/List_of_URI_schemes
						# Permanent or non-application-specific provisional with some exceptions due to wide use.
						'aaa = uri.scheme:URLScheme',
						'aaas = uri.scheme:URLScheme',
						'acap = uri.scheme:URLScheme',
						'afp = uri.scheme:URLScheme',
						'app = uri.scheme:URLScheme',
						'coap = uri.scheme:URLScheme',
						'coaps = uri.scheme:URLScheme',
						'cvs = uri.scheme:URLScheme',
						'dict = uri.scheme:URLScheme',
						'facetime = uri.scheme:URLScheme',
						'feed = uri.scheme:URLScheme',
						'finger = uri.scheme:URLScheme',
						'fish = uri.scheme:URLScheme',
						'git = uri.scheme:URLScheme',
						'imap = uri.scheme:URLScheme',
						'irc6 = uri.scheme:URLScheme',
						'ircs = uri.scheme:URLScheme',
						'ldaps = uri.scheme:URLScheme',
						'market = uri.scheme:URLScheme',
						'mumble = uri.scheme:URLScheme',
						'nntp = uri.scheme:URLScheme',
						'pop = uri.scheme:URLScheme',
						'reload = uri.scheme:URLScheme',
						'rsync = uri.scheme:URLScheme',
						'rtmfp = uri.scheme:URLScheme',
						'rtmp = uri.scheme:URLScheme',
						's3 = uri.scheme:URLScheme',
						'smb = uri.scheme:URLScheme',
						'snmp = uri.scheme:URLScheme',
						'ssh = uri.scheme:URLScheme',
						'svn = uri.scheme:URLScheme',
						'svn+ssh = uri.scheme:URLScheme',
						'teamspeak = uri.scheme:URLScheme',
						'udp = uri.scheme:URLScheme',
						'vnc = uri.scheme:URLScheme',
						'webcal = uri.scheme:URLScheme',
						'ws = uri.scheme:URLScheme',
						'wss = uri.scheme:URLScheme',
						'xri = uri.scheme:URLScheme',
					],
			},
)
