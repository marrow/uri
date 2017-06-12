#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import codecs

try:
	from setuptools.core import setup, find_packages
except ImportError:
	from setuptools import setup, find_packages


if sys.version_info < (2, 7):
	raise SystemExit("Python 2.7 or later is required.")
elif sys.version_info > (3, 0) and sys.version_info < (3, 2):
	raise SystemExit("Python 3.2 or later is required.")

version = description = url = author = version_info = ''  # Actually loaded on the next line; be quiet, linter.
exec(open(os.path.join("uri", "release.py")).read())

here = os.path.abspath(os.path.dirname(__file__))

tests_require = [
		'pytest',  # test collector and extensible runner
		'pytest-cov',  # coverage reporting
		'pytest-flakes',  # syntax validation
		'pytest-catchlog',  # log capture
		'pytest-isort',  # import ordering
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
			"Programming Language :: Python :: 2",
			"Programming Language :: Python :: 2.7",
			"Programming Language :: Python :: 3",
			"Programming Language :: Python :: 3.2",
			"Programming Language :: Python :: 3.3",
			"Programming Language :: Python :: 3.4",
			"Programming Language :: Python :: 3.5",
			"Programming Language :: Python :: 3.6",
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
	
	setup_requires = [
			'pytest-runner',
		] if {'pytest', 'test', 'ptr'}.intersection(sys.argv) else [],
	
	install_requires = [
			'pathlib2; python_version < "3.4"',  # Path manipulation utility.
		],
	
	extras_require = dict(
			http = ['requests'],  # Support for the http:// and https:// protocols.
			development = tests_require + [  # Development-time dependencies.
					'pre-commit',  # Commit hooks for code quality.
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
					],
			},
)
