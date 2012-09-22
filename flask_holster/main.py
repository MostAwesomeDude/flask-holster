from functools import partial, wraps

from flask import g, make_response, request
from flask_holster.exts import ext_dict, guess_type
from flask_holster.mime import Accept
from flask_holster.views import HTMLTemplate, PlainTemplate, templates

def worker(view, *args, **kwargs):
    d = view(*args, **kwargs)
    mime = g.mime.plain()

    overrides = getattr(view, "_holsters", {})
    templater = overrides.get(mime)
    if not templater:
        templater = templates.get(mime, PlainTemplate())

    response = make_response(templater.format(d))
    response.headers["Content-Type"] = mime
    return response


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
    """

    if route.endswith("/"):
        extended = "%s.<ext>/" % route[:-1]
    else:
        extended = "%s.<ext>" % route

    router = app.route(route)
    hrouter = app.route(extended)

    def inner(view):
        p = wraps(view)(partial(worker, view))
        router(p)
        hrouter(p)
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

    This is mostly just attaching hooks.
    """

    app.holster = partial(holster, app)
    app.url_value_preprocessor(holster_url_value_preprocessor)
