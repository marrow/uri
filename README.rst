===
uri
===

    © 2017-2023 Alice Bevan-McGregor and contributors.

..

    https://github.com/marrow/uri

..

    |latestversion| |ghtag| |downloads| |masterstatus| |mastercover| |masterreq| |ghwatch| |ghstar|


Installation
============

Installing ``uri`` is easy, just execute the following in a terminal::

    pip install uri

**Note:** We *strongly* recommend always using a container, virtualization, or sandboxing environment of some kind when
developing using Python; installing things system-wide is yucky (for a variety of reasons) nine times out of ten.  We
prefer light-weight `virtualenv <https://virtualenv.pypa.io/en/latest/virtualenv.html>`__, others prefer solutions as
robust as `Vagrant <http://www.vagrantup.com>`__.

If you add ``uri`` to the ``install_requires`` argument of the call to ``setup()`` in your application's
``setup.py`` file, ``uri`` will be automatically installed and made available when your own application or
library is installed.  We recommend using "less than" version numbers to ensure there are no unintentional
side-effects when updating.  Use ``uri<2.1`` to get all bug fixes for the current release, and
``uri<3.0`` to get bug fixes and feature updates while ensuring that large breaking changes are not installed.

While ``uri`` does not have any hard dependencies on any other package, it is **strongly** recommended that
applications using ``uri`` in web-based applications also install the
`MarkupSafe <https://pypi.org/project/MarkupSafe/>`__ package to provide more efficient string escaping and some
additional functionality.


Development Version
-------------------

    |developstatus| |developcover| |ghsince| |issuecount| |ghfork|

Development takes place on `GitHub <https://github.com/>`__ in the `uri
<https://github.com/marrow/uri/>`__ project.  Issue tracking, documentation, downloads, and test automation
are provided there.

Installing the current development version requires `Git <https://git-scm.com/>`__, a distributed source code
management system.  If you have Git you can run the following to download and *link* the development version into your
Python runtime::

    git clone https://github.com/marrow/uri.git
    (cd uri; python setup.py develop)

You can then upgrade to the latest version at any time::

    (cd uri; git pull; python setup.py develop)

If you would like to make changes and contribute them back to the project, fork the GitHub project, make your changes,
and submit a pull request.  This process is beyond the scope of this documentation; for more information see
`GitHub's documentation <http://help.github.com/>`_.


Getting Started
===============


URI
---

An abstract string-like (and mapping-like, and iterator-like...) identifier for a resource with the regular form
defined by `RFC 3986 <http://pretty-rfc.herokuapp.com/RFC3986>`_::

    scheme:[//[user[:password]@]host[:port]][/path][?query][#fragment]

For details on these components, `please refer to Wikipedia
<https://en.wikipedia.org/wiki/Uniform_Resource_Identifier#Syntax>`__. Each of these components is represented by an
appropriate rich datatype:

* The ``scheme`` of a URI represents an extensible API of string-like plugins.
* Any IPv6 ``host`` is automatically wrapped and unwrapped in square braces.
* The ``path`` is represented by a ``PurePosixPath``.
* The ``query`` is a rich ordered multi-value bucketed mutable mapping called ``QSO``. (Ouch, but that's what it is!)

Instantiate a new URI by passing in a string or string-castable object, ``pathlib.Path`` compatible object, or object
exposing a ``__link__`` method or attribute::

    home = URI("https://github.com/marrow/")

The *scalar* attributes are combined into several *compound* groups for convenience:

* The ``credentials`` are a colon (``:``) separated combination of: ``user`` + ``password`` — also accessible via the
  shorter ``auth`` or the longer ``authentication`` attributes. May be assigned using array/mapping notation.
  Accessing ``uri[user:pass]`` will return a mutated instance with credentials included.
* The ``authority`` part is the combination of: ``credentials`` + ``host`` + ``port``
* The ``heirarchical`` part is the combination of: ``authority`` part + ``path``

Other aliases are provided for the scalar components, typically for compliance with external APIs, such as
interoperability with ``pathlib.Path`` or ``urlsplit`` objects:

* ``username`` is the long form of ``user``.
* ``hostname`` is the long form of ``host``.
* ``authentication`` is the long form of ``auth``.

In addition, several string views are provided for convenience, but ultimately all just call `str()` against the
instance or one of the compound groups described above:

* ``uri`` represents the entire URI as a string.
* ``safe_uri`` represents the entire URI, sans any password that may be present.
* ``base`` is the combination of ``scheme`` and the ``heirarchical`` part.
* ``summary`` is a useful shortcut for web presentation containing only the ``host`` and ``port`` of the URI.
* ``qs`` is just the query string, as a plain string instead of QSO instance.

URI values may be absolute identifiers or relative references. Absolute URIs are what most people see every day:

* ``https://example.com/about/us``
* ``ftp://example.com/thing.txt``
* ``mailto:user@example.com``
* ``uri:ISSN:1535-3613``

Indirect references require the context of an absolute identifier in order to resolve them. Examples include:

* ``//example.com/protocol/relative`` — protocol implied from context, frequently used in HTML when referencing
  resources hosted on content delivery networks.
* ``/host/relative`` — all elements *up to* the path are preserved from context, also frequently used in HTML when
  referencing resources on the same server. This is not equivalent to ``file:///host/relative``, as the protocol is
  unknown.
* ``relative/path`` — the resulting path is relative to the "current working directory" of the context.
* ``../parent/relative/path`` — references may ascend into parents of the context.
* ``resource#fragment`` — referencing a specific fragment of a sibling resource.
* ``#fragment`` — a same-document reference to a specific fragment of the context.

Two primary methods are provided to combine a base URI with another URI, absolute or relative.  The first, utilizing
the ``uri.resolve(uri, **parts)`` method, allows you to both resolve a target URL as well as provide explicit
overrides for any of the above scalar attributes, such as query string. The second, which is recommended for general
use, is to use the division and floor division operators::

    base = URI("https://example.com/about/us")
    cdn = base // "cdn.example.com"
    js = cdn / "script.js"
    css = cdn / "script.css"

Please note that once a URI has an "authority" part (basically, the parts prior to the path such as host) then any
path directly assigned must be "rooted", or contain a leading slash.


Schemes
-------

Each URI has a scheme that should be registered with the `Internet Assigned Numbers Authority (IANA)
<https://en.m.wikipedia.org/wiki/Internet_Assigned_Numbers_Authority>`_ and specifies the mechanics of the URI
fields. Examples include: ``http``, ``https``, ``ftp``, ``mailto``, ``file``, ``data``, etc.

The declaration of which schemes are URL-like (featuring a `://` double-slashed separator) is based on Python's
``entry_points`` plugin registry mapping scheme names to the ``Scheme`` objects used to handle them. If a scheme
renders URI-like when your application requires URL-like, you can `utilize package metadata
<https://packaging.python.org/guides/creating-and-discovering-plugins/#using-package-metadata>`_ to register
additional mappings.

For an example, and to see the core set handled this way, examine the ``setup.py`` and ``setup.cfg`` files within this
project. If you wish to imperatively define schemes, you can do so with code such as the following. It is **strongly
recommended** to not implement this as an *import time side effect*. To mutate the plugin registry directly::

    from uri.scheme import URLScheme
    from uri.part.scheme import SchemePart
    
    SchemePart.registry['amqp'] = URLScheme('amqp')
    SchemePart.registry['amqps'] = URLScheme('amqps')

Subsequent attempts to resolve ``entry_points`` by these names will now resolve to the objects you have specified.


WSGI
----

A WSGI request environment contains all of the details required to reconstruct the requested URI. The simplest example
of why one might do this is to form a "base URI" for relative resolution. WSGI environment-wrapping objects such as
`WebOb's <https://webob.org>`_ ``Request`` class instances may be used as long as the object passed in exposes the
original WSGI environment using an attribute named ``environ``.

To perform this task, use the ``URI.from_wsgi`` factory method::

    from webob import Request

    request = Request.blank('https://example.com/foo/bar?baz=27')
    uri = URI.from_wsgi(request)
    assert str(uri) == 'https://example.com/foo/bar?baz=27'


Migrating
=========

A vast majority of other URI parsers emit plain dictionaries or provide ``as_dict`` methods. URI objects can be
transformed into such using a fairly basic "dictionary comprehension"::

    uri = URI('http://www.example.com/3.0/dd/ff/')
    {i: getattr(uri, i) for i in dir(uri) if i[0] != '_' and not callable(getattr(uri, i))}

The above will produce a dictionary of all URI attributes that are not "private" (prefixed by an underscore) or
executable methods.


From ``furl``
-------------

    https://github.com/gruns/furl

* A majority of the object attributes have parity: ``scheme``, ``username``, ``password``, ``host``, even ``origin``.
* ``furl.args`` -> ``URI.query``
* ``furl.add()``, ``furl.set()``, ``furl.remove()`` -> inline, chained manipulation is not supported.
* ``furl.url`` -> ``str(uri)`` or ``URI.uri``
* ``furl.netloc`` -> ``URI.authority``
* Fragments do not have ``path`` and ``query`` attributes; under ``URI`` the fragment is a pure string.
* ``furl.path`` -> ``URI.path`` where ``furl`` implements its own, ``URI.path`` are PurePosixPath instances.
* ``furl.join`` is accomplished via division operators under ``URI``, or for more complete relative resolution, use
  the ``URI.resolve`` method.
* The ``URI`` class does not currently infer protocol-specific default port numbers.
* Manipulation via division operators preserves query string parameters under ``furl``, however the ``URI`` package
  assumes relative URL resolution, which updates the path and clears parameters and fragment. To extend the path while
  preserving these::
  
      uri = URI('http://www.google.com/base?one=1&two=2')
      uri.path /= 'path'
      assert str(uri) == 'http://www.google.com/base/path?one=1&two=2'


From ``dj-mongohq-url``
-----------------------

    https://github.com/ferrix/dj-mongohq-url

Where your ``settings.py`` file's ``DATABASES`` declaration used ``dj_mongohq_url.config``, instead use::

    from uri.parse.db import parse_dburi
    
    DATABASES = {'default': parse_dburi('mongodb://...')}


From ``django-url-tools``
-------------------------

    https://bitbucket.org/monwara/django-url-tools

The majority of the ``UrlHelper`` attributes are directly applicable to ``URI`` instances, occasionally with minor
differences, typically of naming. The differences are documented here, and "template tags" and "filters" are not
provided for.

* Where ``UrlHelper.path`` are plain strings, ``URI.path`` attributes are `PurePosixPath
  <https://docs.python.org/3/library/pathlib.html#pure-paths>_` instances which support typecasting to a string if
  needed.

* ``UrlHelper.query_dict`` and ``UrlHelper.query`` are replaced with the dict-like ``URI.query`` attribute.

* ``UrlHelper.query_string`` is shortened to ``URI.qs``, additionally, the object retrieved when accessing ``query``
  may be cast to a string as per the rich path representation.

* ``UrlHelper.get_full_path`` -- equivalent to the ``URI.resource`` compound, combining path, query string, and
  fragment identifier.

* ``UrlHelper.get_full_quoted_path`` -- alternative currently not provided.

* There are no direct equivalents provided for:

  * ``UrlHelper.hash`` -- **not** provided due to FIPS-unsafe dependence on MD5.
  * ``UrlHelper.get_query_string`` -- encoding is handled automatically.
  * ``UrlHelper.get_query_data`` -- this helper for subclass inheritance is not provided.
  * ``UrlHelper.update_query_data`` -- manipulate the query directly using ``URI.query.update``.
  * ``UrlHelper.overload_params`` -- can be accomplished using modern dictionary merge literal syntax.
  * ``UrlHelper.toggle_params`` -- this seems an unusual use case, and can be resolved similarly to the last.
  * ``UrlHelper.get_path`` -- unnecessary, access ``URI.path`` directly.
  * ``UrlHelper.del_param`` and ``UrlHelper.del_params`` -- just utilize the ``del`` keyword (or ``pop`` method) on/of
    the ``URI.query`` attribute.


From ``url2vapi``
-----------------

    https://github.com/Drachenfels/url2vapi

Where ``url2vapi`` provides a dictionary of parsed URL components, with some pattern-based extraction of API metadata,
``URI`` provides a rich object with descriptor attributes. Version parsing can be accomplished by extracting the
relevant path element and parsing it::

    from pkg_resources import parse_version
    from uri import URI
    
    url = 'http://www.example.com/3.0/dd/ff/'
    uri = URI(url)
    version = parse_version(uri.path.parts[1])

The ``ApiUrl`` class otherwise offers no functionality. The minimal "data model" provided only accounts for:

* ``protocol`` -> ``scheme``
* ``port`` is common, though URI port numbers are stored as integers, not strings.
* ``domain`` -> ``host``
* ``remainder`` does not have an equivalent; there are several compound getters which may provide similar results.
* ``kwargs`` also has no particular equivalent. URI instances are not "arbitrarily extensible".
* Parsing of URL "parameters" incorrectly assume these are exclusive to the referenced resource, as per query string
  arguments, when each path element may have its own distinct parameters. The difference between::
  
      https://example.com/foo/bar/baz?prop=27
      https://example.com/foo/bar/baz;prop=27
  
  And::
  
      https://example.com/foo;prop=27/bar/baz;prop=27
      https://example.com/foo/bar;prop=27/baz
      https://example.com/foo/bar/baz;prop=27


From ``url-parser``
-------------------

    https://github.com/AdaptedAS/url_parser

* ``protocol`` -> ``scheme``
* ``www`` has no equivalent; check for ``URI.host.startswith('www.')`` instead.
* ``sub_domain`` has no equivalent; parse/split ``URI.host`` instead.
* ``domain`` -> ``host``
* ``top_domain`` has no equivalent; as per ``sub_domain``.
* ``dir`` -> ``path``
* ``file`` -> ``path``
* ``fragment`` is unchanged.
* ``query`` -> ``qs`` for the string form, ``query`` for a rich ``QSO`` instance interface.


From ``p.url``
--------------

    https://github.com/ultrabluewolf/p.url/

There may be a noticeable trend arising from several sections of "migrating from". Many seem to have accessor or
manipulation **methods** to mutate the object, rather than utilizing native data type interactions, this one does not
buck the trend. Additionally, many of the "attributes" of ``Purl`` are provided as invokable getter/setter methods,
not as static attributes nor automatic properties. In this comparison, attributes trailed by parenthesis are actually
methods, if ``[value]`` may be passed, the method is also the setter. Lastly, it provides its own ``InvalidUrlError``
which does not subclass ``ValueError``.

The result is a bit of a hodgepodge API that feels more at home in Java.

* ``Purl.query`` is a plain dictionary attribute, not a getter method. Now a rich dict-like ``QSO`` object.
* ``Purl.querystring()`` -> ``URI.qs`` -- pure getter method in ``Purl``.
* ``Purl.add_query()`` and ``Purl.delete_query()`` -- just manipulate ``URI.query`` as a dictionary.
* An alternative to ``param`` for manipulation of path parameters is not provided, as these are protocol-defined.
* ``Purl.protocol([value])`` -> ``URI.scheme``
* ``Purl.hostname([value])`` -> ``URI.host``
* ``Purl.port([value])`` -> ``URI.port``
* ``Purl.path([value])`` -> ``URI.path``
* "Parameter expansion" (which is unrelated to actual URI path element parameters) is not currently supported;
  recommended to simply use f-strings or ``str.format`` as appropriate. As curly braces have no special meaning to
  ``URI``, you may populate these within one for later ``str(uri).format(...)`` interpolation.


From ``url``
------------

    https://github.com/seomoz/url-py

The ``url`` package bundles Cython auto-generated C++ extensions. I do not understand why.

It's nearly 16,000 lines of code.

Sixteen thousand.

A number of attributes are common such as ``scheme``, ``host``, ``hostname``, ``port``, etc.

* ``URL.pld`` and ``URL.tld`` are left as an exercise for the reader.
* ``URL.params`` is not currently implemented.
* ``URL.query`` -> ``URI.qs`` with ``URI.query`` providing a rich dict-like interface.
* ``URL.unicode`` and ``URL.utf8`` are unimplemented. Native ``URI`` storage is Unicode, it's up to you to encode.
* ``URL.strip()`` is unnecessary under ``URI``; empty query strings, fragments, etc., naturally will not have
  dividers. What many might consider to be an "invalid" query string often are not; an encoding for HTTP key-value
  pairs is suggested for the HTTP scheme, however everything after the ``?`` is just a single string, up to server-
  side interpretation. ``?????a=1`` is "perfectly fine".
* Re-ordering of query string parameters is not implemented; the need is dubious at this level.
* ``URL.deparam()`` may be implemented by using `del` to remove known query string arguments, or using the ``pop()``
  method to safely remove arguments that may only be conditionally present, while avoiding exceptions.
* ``URL.abspath()`` is not currently implemented; to be implemented within ``URI.resolve()``.
* ``URL.unescape()`` is not currently implemented.
* ``URL.relative()`` may be implemented more succinctly using division operators, e.g. ``base / target``. This also
  supports HTTP reference protocol-relative resolution using the floor division operator, e.g. ``base // target``.
* ``URL.punycode()`` and ``URL.unpunycode()`` are not implemented, as the goal is for Unicode to be natively/naturally
  supported with Punycode encoding automatic at instantiation and serialization to string time, reference `#18
  <https://github.com/marrow/uri/issues/18>`_.



Version History
===============

Version 3.0.0
-------------

* Improved documentation, notably, incorporated the imperative registration of schemes example from `#14
  <https://github.com/marrow/uri/issues/14#issuecomment-667567337>`_.
* Inclusion of adaption utilities and tests obviating the need for other utility packages, and documented migration
  from several other URI or URL implementations.
* Removed legacy Python 2 support adaptions.
* Removed Python 3 support less than Python 3.8 due to type annotation functionality and syntax changes.
* Broad adoption of type hinting annotations across virtually all methods and instance attributes.
* Updated ABC import path references to correct Python 3.9 warnings.
* Added syntax sugar for assignment of URI authentication credentials by returning a mutated instance when sliced. `#10
  <https://github.com/marrow/uri/issues/10>`_
* Additional ``__slots__`` declarations to improve memory efficiency.
* Added RFC example relative resolutions as tests; we are a compatible resolver, not a strict one.
* Added ability to construct a URI from a populated WSGI request environment to reconstruct the requested URI. WebOb
  added as a testing dependency to cover this feature. `#13 <https://github.com/marrow/uri/issues/13>`_
* Migrated from Travis-CI to GitHub Actions for test runner automation.
* Added a significant number of additional pre-registered URL-like (``://``) schemes, based on Wikipedia references.
* Automatically utilize Punycode / IDNA encoding of internationalized domain names, ones containing non-ASCII. `#18
  <https://github.com/marrow/uri/issues/18>`_


Version 2.0.1
-------------

* Added non-standard `resource` compound view.
* Removed Python 3.3 support, added 3.7, removed deprecated testing dependency.
* Scheme objects hash as per their string representation. `#5 <https://github.com/marrow/uri/issues/5>`_
* Dead code clean-up.
* Additional tests covering previously uncovered edge cases, such as assignment to a compound view property.
* Restrict assignment of rootless paths (no leading `/`) if an authority part is already present. `#8
  <https://github.com/marrow/uri/issues/8>`_
* Enable handling of the following schemes as per URL (colon + double slash):
	* sftp
	* mysql
	* redis
	* mongodb


Version 2.0
-----------

* Extraction of the ``URIString`` object from Marrow Mongo.


Version 1.0
-----------

* Original package by Jacob Kaplan-Moss. Copyright 2008 and released under the BSD License.


License
=======

The URI package has been released under the MIT Open Source license.

The MIT License
---------------

Copyright © 2017-2023 Alice Bevan-McGregor and contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the “Software”), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

.. |ghwatch| image:: https://img.shields.io/github/watchers/marrow/uri.svg?style=social&label=Watch
    :target: https://github.com/marrow/uri/subscription
    :alt: Subscribe to project activity on Github.

.. |ghstar| image:: https://img.shields.io/github/stars/marrow/uri.svg?style=social&label=Star
    :target: https://github.com/marrow/uri/subscription
    :alt: Star this project on Github.

.. |ghfork| image:: https://img.shields.io/github/forks/marrow/uri.svg?style=social&label=Fork
    :target: https://github.com/marrow/uri/fork
    :alt: Fork this project on Github.

.. |masterstatus| image:: http://img.shields.io/travis/marrow/uri/master.svg?style=flat
    :target: https://travis-ci.org/marrow/uri/branches
    :alt: Release build status.

.. |mastercover| image:: http://img.shields.io/codecov/c/github/marrow/uri/master.svg?style=flat
    :target: https://codecov.io/github/marrow/uri?branch=master
    :alt: Release test coverage.

.. |masterreq| image:: https://img.shields.io/requires/github/marrow/uri.svg
    :target: https://requires.io/github/marrow/uri/requirements/?branch=master
    :alt: Status of release dependencies.

.. |developstatus| image:: http://img.shields.io/travis/marrow/uri/develop.svg?style=flat
    :target: https://travis-ci.org/marrow/uri/branches
    :alt: Development build status.

.. |developcover| image:: http://img.shields.io/codecov/c/github/marrow/uri/develop.svg?style=flat
    :target: https://codecov.io/github/marrow/uri?branch=develop
    :alt: Development test coverage.

.. |developreq| image:: https://img.shields.io/requires/github/marrow/uri.svg
    :target: https://requires.io/github/marrow/uri/requirements/?branch=develop
    :alt: Status of development dependencies.

.. |issuecount| image:: http://img.shields.io/github/issues-raw/marrow/uri.svg?style=flat
    :target: https://github.com/marrow/uri/issues
    :alt: Github Issues

.. |ghsince| image:: https://img.shields.io/github/commits-since/marrow/uri/2.0.0.svg
    :target: https://github.com/marrow/uri/commits/develop
    :alt: Changes since last release.

.. |ghtag| image:: https://img.shields.io/github/tag/marrow/uri.svg
    :target: https://github.com/marrow/uri/tree/2.0.0
    :alt: Latest Github tagged release.

.. |latestversion| image:: http://img.shields.io/pypi/v/uri.svg?style=flat
    :target: https://pypi.python.org/pypi/uri
    :alt: Latest released version.

.. |downloads| image:: http://img.shields.io/pypi/dw/uri.svg?style=flat
    :target: https://pypi.python.org/pypi/uri
    :alt: Downloads per week.

.. |cake| image:: http://img.shields.io/badge/cake-lie-1b87fb.svg?style=flat
