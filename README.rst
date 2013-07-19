=============
Flask-Holster
=============

This is Holster, an extension for Flask that makes RESTfulness and content
negotiation easy::

    from flask import Flask
    from flask.ext.holster.main import init_holster

    app = Flask(__name__)
    init_holster(app)

    @app.holster("/test")
    def test():
        from math import pi

        return {
            "data": "Hello from Holster!",
            "nested": {
                "numeric": 0,
                "floating": pi,
                "unicode": u"Espa\xf1ol",
            },
            "secure": {
                "xss-sword": ';!--"<XSS>=&{()}',
            }
        }

    if __name__ == "__main__":
        app.run()

This application will automatically figure out which data type to return,
using a combination of user agent parameters and URL extensions. If a user
agent requests "/test.html" they will get HTML, but if they request
"/test.json" they will get JSON instead. No longer do you have to worry about
constructing sites with separate interfaces for HTML and JSON; one holstered
site can do it all!

Holster currently has default renderers for the following formats:

 * HTML
 * JSON
 * Plaintext
 * YAML (with optional PyYAML support for prettified YAML)

These default renderers are provided mostly for bootstrapping and development,
although the JSON and YAML renderers are likely very similar to the renderers
that one might desire in production.

Tips & Tricks
=============

Defining a New Format
---------------------

Adding new renderers for a format is done in an ad-hoc manner. Users can also
override renderers for any format or MIME type they would like, with
``with_template``::

    from my_sweet_website import PNGHeaderMaker
    from flask.ext.holster.main import with_template

    @app.holster("/customized")
    @with_template("image/png", PNGHeaderMaker)
    def custom():
        return {"header": "Welcome to my site!"}

There isn't currently a way to add a renderer which covers an entire
application. That should really be fixed at some point...

Forcing a Renderer
------------------

Sometimes one wants ``url_for()`` to pick a particular renderer for a target
endpoint, instead of letting Holster and the user agent negotiate a particular
format. This is relatively straightforward; just adjust the endpoint slightly
and explain which extension you want to use::

    from flask import url_for

    @app.holster("/force")
    def force():
        return {
            "url": url_for("sabers", style="cutlass"),
            "html_url": url_for("sabers-ext", ext="html", style="cutlass"),
        }

In this example, the ``"sabers-ext"`` endpoint is just like ``"sabers"``, but
requires an additional argument, ``ext``, which contains the extension to use.
This allows generation of URLs for endpoints which have fine-grained control
over the preferred output formats.

Changelog
=========

0.3.3
-----

 * Bugfix: Multiple holsterings of a single view in Flask 0.10 and newer were
   causing Flask to refuse to register views due to an internal assertion
   being triggered.
 * Feature: The ``"title"`` key now holds special significance: it will be
   used for titles in built-in renderers, if the renderer supports the notion
   of a title.

0.3.2
-----

 * Bugfix: Custom templaters were being incorrectly unused if they were not
   HTML or JSON templaters.
 * Feature: Allow "svg" as an extension for the "image/svg+xml" MIME type.

0.3.1
-----

 * Bugfix: Remove extraneous debugging statements.

0.3
---

 * Compatibility: Require vcversioner for version numbers.
 * Compatibility: The handwritten MIME parser has been removed in favor of the
   one in Werkzeug. As a result, Flask-Holster is slightly smaller and should
   handle corner cases slightly better.
 * Bugfix: Always define a YAML conversion. For pretty YAML, install PyYAML.
   YAML output is now always enabled, using JSON as a fallback when PyYAML is
   not available. PyYAML is *not* required and is not in the
   `requirements.txt`.

0.2.5
-----

 * Feature: ``init_holster()`` now works on Flask blueprints as well as Flask
   applications.

0.2.4
-----

 * Bugfix: Correctly omit trailing colons (and related recursion) on list
   items in the default HTML view template.

0.2.3
-----

 * Bugfix: Permit kwargs in routing decorators, including ``methods``. 
 * Bugfix: Pass along premade responses as-is without any interference.
   Permits things like ``redirect()`` inside otherwise-rigid controllers.

0.2.2
-----

 * Bugfix: Pass along names inside ``lift()`` to correctly name reversed
   routes

0.2.1
-----

 * Bugfix: Specialize extended routes for "/" to avoid malformed routes

0.2
---

 * Compatibility: Don't use itertools, for Python 2.5
 * Enhancement: Split holsterizing views into two pieces, for easier
   customization
 * Feature: New helpers module for helping write customized views

1.1.2
-----

 * Feature: Changelog
 * Feature: Documentation
 * Feature: Optional ``HOLSTER_COMPRESS`` setting for automatically
   compressing response data
 * Enhancement: Vary header is filled out
 * Change: Improved names of view objects
