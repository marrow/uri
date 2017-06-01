import warnings

try:
	from setuptools.core import setup
except ImportError:
	try:
		from setuptools import setup
	except ImportError:
		from distutils.core import setup

warnings.warn("""The 'uri' package will be changing drastically in the near future.
	As a result you will need to pin the version to 'uri<2.0' to avoid issues.""",
	FutureWarning)

setup(
	name = "uri",
	version = "1.0.1",
	description = "A library for URI handling featuring an implementation of URI-Templates",
	author = 'Jacob Kaplan-Moss',
	author_email = 'jacob@jaobian.org',
	maintainer = 'Alice Bevan-McGregor',
	maintainer_email = 'alice@gothcandy.com',
	py_modules = ['uri'],
	classifiers = [
		'Development Status :: 1 - Planning',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Internet',
	]
)
