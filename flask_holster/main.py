from functools import partial

from flask import g, make_response, request
from flask_holster.exts import guess_type
from flask_holster.mime import Accept, MIME
from flask_holster.views import PlainTemplate, templates

def worker(view):
    def inner(*args, **kwargs):
        d = view(*args, **kwargs)
        mime = g.mime.plain()

        template = templates.get(mime, PlainTemplate)
        templater = template()

        response = make_response(templater.format(d))
        response.headers["Content-Type"] = mime
        return response
    return inner


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
        types.types.insert(0, MIME.from_string(guess_type(ext)))

    accept = Accept(request.headers["accept"])

    mime = accept.best(types)

    g.mime = mime


def holsterize(app):
    app.holster = partial(holster, app)
    app.url_value_preprocessor(holster_url_value_preprocessor)
