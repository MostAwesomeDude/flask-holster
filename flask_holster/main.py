from functools import partial

from flask import g, request
from flask_holster.exts import ext_dict, guess_type
from flask_holster.mime import Accept
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


def holster(app, route):
    """
    Decorator which replaces ``route()``.

    This decorator is nested because it is meant to be called in the same
    style as ``route()``:

        @app.holster("/")
        def index():
            pass
    """

    def inner(view):
        wrapped = holsterize(app, view)
        # This returns the wrapped view. We don't care about it though.
        bare_holster(app, route)(wrapped)

        # Return the original view so that people can do more things with it.
        # Even if they re-holster the view, it's gonna be way easier for us to
        # do things if we don't multiply-wrap it.
        return view

    return inner


def holster_url_value_preprocessor(endpoint, values):
    types = Accept(",".join(templates))
    if values and "ext" in values:
        ext = values.pop("ext")
        types.prefer(guess_type(ext))

    accept = Accept(request.headers["accept"])

    mime = accept.best(types)

    g.mime = mime


def init_holster(app):
    """
    Initialize a Flask to have holsters.

    This is mostly just attaching hooks and setting default configuration
    values.
    """

    app.bare_holster = partial(bare_holster, app)
    app.holster = partial(holster, app)
    app.holsterize = partial(holsterize, app)
    app.url_value_preprocessor(holster_url_value_preprocessor)

    app.config.setdefault("HOLSTER_COMPRESS", False)
