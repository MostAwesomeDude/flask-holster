=============
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

There isn't currently a way to register renderers which cover an entire
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
