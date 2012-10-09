from functools import partial, wraps
from zlib import compress

from flask import g, make_response, request
from flask_holster.views import Str, templates


def _worker(app, view, *args, **kwargs):
    """
    The actual worker.
    """

    d = view(*args, **kwargs)
    mime = g.mime.plain()

    overrides = getattr(view, "_holsters", {})
    templater = overrides.get(mime)
    if not templater:
        templater = templates.get(mime, Str())

    # Run the templater.
    data = templater.format(d)

    # Optionally compress the data.
    if app.config["HOLSTER_COMPRESS"] and "deflate" in request.accept_encodings:
        # It's possible that our data is Unicode. Thanks, Jinja. In that case,
        # turn it into UTF-8 before compressing.
        if isinstance(data, unicode):
            data = data.encode("utf-8")
        data = compress(data)
        compressed = True
    else:
        compressed = False

    # Use the formatted data as the response body.
    response = make_response(data)

    # Indicate the MIME type of the data that we are sending back.
    response.headers["Content-Type"] = mime

    # Indicate to caches that the data returned is dependent on the Accept
    # header's value in the request.
    response.vary.add("Accept")

    # Fill out the compression header and indicate varyings, if needed.
    if compressed:
        response.headers["Content-Encoding"] = "deflate"
        response.vary.add("Accept-Encoding")

    return response


def holsterize(app, view):
    """
    Wrap a view with a holster.
    """

    p = wraps(view)(partial(_worker, app, view))

    return p


def bare_holster(app, route):
    """
    Decorator which replaces ``route()``.

    This decorator is nested because it is meant to be called in the same
    style as ``route()``:

        @app.bare_holster("/")
        def index():
            pass

    This is the core functionality of routing; it does not include the logic
    for holstering views, only for attaching them to the app.
    """

    if route.endswith("/"):
        extended = "%s.<ext>/" % route[:-1]
    else:
        extended = "%s.<ext>" % route

    def inner(view):
        name = view.__name__
        app.add_url_rule(route, endpoint=name, view_func=view)
        app.add_url_rule(extended, endpoint="%s-ext" % name, view_func=view)
        return view

    return inner
