About
=====

A library for simple URI handling. It has no external dependancies, and works
with Python 2.3+.

Currently contains only an implementation of URI-Templates
(http://bitworking.org/projects/URI-Templates/) -- but see the TODO_ below.

Some bits are inspired by or based on:

    * Joe Gregorio's example implementation
      (http://code.google.com/p/uri-templates/)

    * Addressable (http://addressable.rubyforge.org/)

Examples
========

Simple usage::

    >>> import uri
    
    >>> args = {'foo': 'it worked'}
    >>> uri.expand_template("http://example.com/{foo}", args)
    'http://example.com/it%20worked'

    >>> args = {'a':'foo', 'b':'bar', 'a_b':'baz'}
    >>> uri.expand_template("http://example.org/{a}{b}/{a_b}", args)
    'http://example.org/foobar/baz'
    
You can also use keyword arguments for a more pythonic style::
    
    >>> uri.expand_template("http://example.org/?q={a}", a="foo")
    'http://example.org/?q=foo'

Contributing
============

I use Mercurial; the canonical repository lives at
http://toys.jacobian.org/hg/uri. Please feel free to send patches or links to
other branches to <jacob@jacobian.org>

TODO
----

Over time, I'd like to add the following features to this library:

    * ``uri.extract(template, uri)``: extract a dict of info given a template
      and a URI.
      
    * ``uri.parse(uri)``: thin wrapper around ``urlparse.urlparse()`` that
      returns a class (so you can do e.g. ``some_uri.fragment`` or whathaveyou.)
      This URI class should have expand/extract methods.
      
    * Add methods/functions to do sane URI joining -- ``urlparse.urljoin`` 
      *never* does what I think it's going to do, especially when faced
      with relative URIs.