========================
Writing Custom Renderers
========================

Holster's flexibility and power is in the hands of developers with custom
renderers. Rather than force users to convolute their data, Holster permits
every handler to register a custom renderer for any format.

Renderers are pretty simple. Extremely simple, actually. Any object which has
a callable attribute named ``format()`` is a renderer. ``format()`` will be
called with a single argument, which is the mapping of data to render.

As an example, here is the default JSON renderer, which simply dumps the
entire mapping using the ``json`` module::

    from flask import json

    class JSONRenderer(object):
        def format(self, d):
            return json.dumps(d)

    json_renderer = JSONRenderer()

And that's it! This renderer is implemented as a class in case it needs to be
customized in the future, but otherwise it should be completely obvious how it
works. Aside from some simplifications, this is actually the code that renders
JSON inside Holster. It's that easy!
