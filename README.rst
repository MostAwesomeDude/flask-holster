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
 * YAML

Users can also override renderers for any format or MIME type they would like,
with ``with_template``::

    from my_sweet_website import PNGHeaderMaker
    from flask.ext.holster.views import with_template

    @app.holster("/customized")
    @with_template("image/png", PNGHeaderMaker)
    def custom():
        return {"header": "Welcome to my site!"}

Changelog
=========

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
