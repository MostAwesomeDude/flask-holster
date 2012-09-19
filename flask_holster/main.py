from functools import partial

from flask import g, make_response, request
from flask_holster.exts import guess_type
from flask_holster.mime import Accept
from flask_holster.views import PlainTemplate, templates

def worker(view):
    def inner(*args, **kwargs):
        d = view(*args, **kwargs)

        template = templates.get(g.mime, PlainTemplate)
        templater = template()

        response = make_response(templater.format(d))
        response.headers["Content-Type"] = g.mime
        return response
    return inner


def holster(app, route):
    """
    Decorator which replaces ``route()``.
    """

    router = app.route(route)
    hrouter = app.route("%s.<ext>" % route)

    def inner(view):
        router(worker(view))
        hrouter(worker(view))

    return inner


def holster_url_value_preprocessor(endpoint, values):
    if "ext" in values:
        ext = values.pop("ext")
        preferred = guess_type(ext)
    else:
        preferred = "text/plain"

    accept = Accept(request.headers["accept"])

    mime = accept.best([preferred])

    g.mime = mime


def holsterize(app):
    app.holster = partial(holster, app)
    app.url_value_preprocessor(holster_url_value_preprocessor)
