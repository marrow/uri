===
uri
===

    © 2017 Alice Bevan-McGregor and contributors.

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
side-effects when updating.  Use ``uri<3.1`` to get all bugfixes for the current release, and
``uri<3.0`` to get bugfixes and feature updates while ensuring that large breaking changes are not installed.

While uri does not have any hard dependencies on any other package, it is **strongly** recommended that applications
using uri in web-based applications also install the ``markupsafe`` package to provide more efficient string escaping and
some additional functionality.


Development Version
-------------------

    |developstatus| |developcover| |ghsince| |issuecount| |ghfork|

Development takes place on `GitHub <https://github.com/>`__ in the
`uri <https://github.com/marrow/uri/>`__ project.  Issue tracking, documentation, and downloads
are provided there.

Installing the current development version requires `Git <http://git-scm.com/>`__, a distributed source code management
system.  If you have Git you can run the following to download and *link* the development version into your Python
runtime::

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
appropraite rich datatype:

* The ``scheme`` of a URI represents an extensible API of string-like plugins.
* Any IPv6 ``host`` is automatically wrapped and unwrapped in square braces.
* The ``path`` is represented by a ``PurePosixPath``.
* The ``query`` is a rich ordered multi-value bucketed mutable mapping called ``QSO``. (Ouch, but that's what it is!)

Instantiate a new URI by passing in a string or string-castable object, ``pathlib.Path`` compatible object, or object
exposing a ``__link__`` method or attribute::

    home = URI("https://github.com/marrow/")

The *scalar* attributes are combined into several *compound* groups for convienence:

* The ``credentials`` are a colon (``:``) separated combination of: ``user`` + ``password`` — also accessible via the
  shorter ``auth`` or the longer ``authentication`` attributes.
* The ``authority`` part is the combination of: ``credentials`` + ``host`` + ``port``
* The ``heirarchical`` part is the combination of: ``authority`` part + ``path``

Other aliases are provided for the scalar components, typically for compliance with external APIs, such as
interoperability with ``pathlib.Path`` or ``urlsplit`` objects:

* ``username`` is the long form of ``user``.
* ``hostname`` is the long form of ``host``.
* ``authentication`` is the long form of ``auth``.

In addition, several string views are provided for convienence, but ultimately all just call `str()` against the
instance or one of the compound groups described above:

* ``uri`` represents the entire URI as a string.
* ``safe_uri`` represents the enture URI, sans any password that may be present.
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


Schemes
-------

Each URI has a scheme which should be registered with the `Internet Assigned Numbers Authority (IANA)
<https://en.m.wikipedia.org/wiki/Internet_Assigned_Numbers_Authority>`_ which specifies the mechanics of the URI
fields.  Examples include: ``http``, ``https``, ``ftp``, ``mailto``, ``file``, ``data``, etc.


Version History
===============

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

Copyright © 2017 Alice Bevan-McGregor and contributors.

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

.. |ghsince| image:: https://img.shields.io/github/commits-since/marrow/uri/1.0.1.svg
    :target: https://github.com/marrow/uri/commits/develop
    :alt: Changes since last release.

.. |ghtag| image:: https://img.shields.io/github/tag/marrow/uri.svg
    :target: https://github.com/marrow/uri/tree/1.0.1
    :alt: Latest Github tagged release.

.. |latestversion| image:: http://img.shields.io/pypi/v/uri.svg?style=flat
    :target: https://pypi.python.org/pypi/uri
    :alt: Latest released version.

.. |downloads| image:: http://img.shields.io/pypi/dw/uri.svg?style=flat
    :target: https://pypi.python.org/pypi/uri
    :alt: Downloads per week.

.. |cake| image:: http://img.shields.io/badge/cake-lie-1b87fb.svg?style=flat
