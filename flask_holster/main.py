from functools import partial

from flask import request
from flask_holster.mime import Accept

def worker(view):
    def inner(*args, **kwargs):
        a = Accept(request.headers["accept"])
        print a
        return view(*args, **kwargs)
    return inner

def holster(app, route):
    """
    Decorator which replaces ``route()``.
    """

    router = app.route(route)

    def inner(view):
        return router(worker(view))

    return inner

def holsterize(app):
    app.holster = partial(holster, app)
