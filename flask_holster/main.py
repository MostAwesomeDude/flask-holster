from functools import partial

from flask import g, request
from flask_holster.exts import ext_dict, guess_type
from flask_holster.mime import preferring
from flask_holster.parts import bare_holster, holsterize
from flask_holster.views import HTMLTemplate, templates


def with_template(mime, templater):
    """
    Decorator to add a customized templater to a holstered view.

    This decoration must happen prior to the holstering:

        @app.holster("/example")
        @with_template("html", HTMLTemplater("example.html"))
        def example():
            return {}
    """

    # Extensions are allowed too!
    if mime in ext_dict:
        mime = ext_dict[mime]

    def attach(f):
        d = getattr(f, "_holsters", {})
        d[mime] = templater
        f._holsters = d
        return f
    return attach


def html_template(template):
    return with_template("text/html", HTMLTemplate(template=template,
        from_string=False))


def holster(app, route, **kwargs):
    """
    Decorator which replaces ``route()``.

    This decorator is nested because it is meant to be called in the same
    style as ``route()``:

        @app.holster("/")
        def index():
            pass
    """

    def inner(view):
        wrapped = holsterize(view)
        # This returns the wrapped view. We don't care about it though.
        bare_holster(app, route, **kwargs)(wrapped)

        # Return the original view so that people can do more things with it.
        # Even if they re-holster the view, it's gonna be way easier for us to
        # do things if we don't multiply-wrap it.
        return view

    return inner


def holster_url_value_preprocessor(endpoint, values):
    """
    Figure out which MIME type should be returned, and prepare the value for
    later processing.
    """

    # Check to see if this has already happened, e.g. in a blueprint.
    if hasattr(g, "_holster_mime"):
        return

    accept = request.accept_mimetypes

    # If the file extension was in there, then prefer a type based on the
    # extension.
    if values and "ext" in values:
        ext = values.pop("ext")
        accept = preferring(guess_type(ext), accept)

    g._holster_mime = accept.best_match(templates.keys())


def init_holster(app):
    """
    Initialize a Flask application or blueprint to have holsters.

    This is mostly just attaching hooks and setting default configuration
    values.
    """

    app.bare_holster = partial(bare_holster, app)
    app.holster = partial(holster, app)
    app.holsterize = holsterize
    app.url_value_preprocessor(holster_url_value_preprocessor)

    if hasattr(app, "config"):
        app.config.setdefault("HOLSTER_COMPRESS", False)
