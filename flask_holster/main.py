from functools import partial

from flask import g, make_response, request
from flask_holster.exts import ext_dict, guess_type
from flask_holster.mime import Accept
from flask_holster.views import HTMLTemplate, PlainTemplate, templates

def worker(view):
    def inner(*args, **kwargs):
        print view
        d = view(*args, **kwargs)
        mime = g.mime.plain()

        overrides = getattr(view, "_holsters", {})
        templater = overrides.get(mime)
        if not templater:
            templater = templates.get(mime, PlainTemplate())

        response = make_response(templater.format(d))
        response.headers["Content-Type"] = mime
        return response
    return inner


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
        router(worker(view))
        hrouter(worker(view))

    return inner


def holster_url_value_preprocessor(endpoint, values):
    types = Accept(",".join(templates))
    if values and "ext" in values:
        ext = values.pop("ext")
        types.prefer(guess_type(ext))

    accept = Accept(request.headers["accept"])

    mime = accept.best(types)

    g.mime = mime


def holsterize(app):
    app.holster = partial(holster, app)
    app.url_value_preprocessor(holster_url_value_preprocessor)
