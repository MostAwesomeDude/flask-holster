from functools import partial

def holster(app, route):
    return app.route(route)

def holsterize(app):
    app.holster = partial(holster, app)
