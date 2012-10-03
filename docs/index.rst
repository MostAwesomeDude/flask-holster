.. Flask-Holster documentation master file, created by
   sphinx-quickstart on Sat Sep 22 11:58:01 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=============
Flask-Holster
=============

Introduction
============

Flask-Holster, or Holster for short, is a simple Flask extension for
performing automated content negotiation with rigid MVC on ordinary request
handlers.

Holster in 3 Lines
==================

In a nutshell::

    @app.holster("/route/<arg>")
    def route(arg):
        return {"argument": arg}

What just happened?
===================

This snippet creates a route, ``/route/<arg>`` in the same way as a normal
Flask route, and it also creates an extra route, ``/route/<arg>.<ext>``. This
extra route can capture a file extension.

When a request comes in for this handler, Holster determines which type of
data it will return, and then runs the handler normally. The handler returns a
**mapping** of some sort, like a ``dict``, and then Holster renders that
mapping into the desired type and returns it with the appropriate headers.

In MVC terms, Holster separates the model and view in a rigid, completely
enforced manner. The data returned from the request handler is independent of,
and compatible with, all of the view renderers which can render it.

Why is this a good thing?
=========================

The original motivation here is creating RESTful APIs. For many modern
programmers working on the Web, "REST API" is a buzzphrase that deciphers
roughly to "stateless JSON-based low-level API over HTTP *which is not the
same as my actual website*." This is a very unfortunate reading because HTTP
and REST are vastly more powerful and flexible than this. When the Web was
formalized, a few forward-thinking framers wrote in the ability for the user
agent (a client) and the Web application (a server) to **negotiate content
metadata**, including language, encoding, format, and so forth.

Holster can return both JSON and HTML formats from a given set of data. This
means that programmers can write a single site once, and instantly gain a
JSON-based interface for free.

Of course, there's no such thing as a free lunch. The site still probably
needs to be structured in a way that fits how you want the data to be
formatted. Even so, Holster makes this easy.

Where should I get started?
===========================

Holster's enhancements are per-handler. If you want to dive in and try out
Holster on your site, it's only three simple steps.

Step 1: Download Holster
------------------------

Holster is on PyPI; run ``pip install Flask-Holster``.

Step 2: Holsterize your App
---------------------------

When you create your Flask application object, init Holster::

    from flask import Flask
    from flask.ext.holster.main import init_holster

    app = Flask(__name__)
    init_holster(app)

Step 3: Holsterize your Handlers
--------------------------------

Simply go from this::

    @app.route("/<foo>/<bar>/baz")
    def baz(foo, bar):
        return render_template("baz.html", foo=foo, bar=bar)

To this::

    from flask.ext.holster.simple import html

    @app.holster("/<foo>/<bar>/baz")
    @html("baz.html")
    def baz(foo, bar):
        return {"foo": foo, "bar": bar}

.. toctree::
   :maxdepth: 2

   renderers
   escape
   api



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

