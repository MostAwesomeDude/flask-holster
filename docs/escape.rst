================
Escaping Holster
================

Holster is rigid. This means that there will be times when one wishes to do
things, but cannot do them because Holster is in the way. Fortunately, it is
possible to escape Holster's control.

Step 0: Do You Need Holster?
============================

First, ask yourself: "Do I *need* Holster for this view?" Holster only
operates on a per-view basis, and each view must explicitly ask for holstering
via ``holster()`` (or other mechanisms, detailed below.) If you don't need
Holster, don't use it. It's okay; Holster doesn't have feelings and won't feel
neglected if you don't use it on a view.

Step 1: Altering the Response
=============================

So, you need to adjust the response slightly. Maybe there's a header that you
need to set, or you want to do some brief accounting. Whatever the reason is,
you want to do it on one single specific view, and so you don't want to abuse
Flask's global response hooks.

The solution is easy. Break Holster's decorator into two steps, and insert
your function between them.

Starting with something like::

    @app.holster("/escape")
    def escape():
        return {}

This is equivalent::

    @app.bare_holster("/escape")
    @app.holsterize
    def escape():
        return {}

And now, using ``lift()`` from ``flask.ext.holster.helpers``, let's disable
caching, as an example::

    def no_cache(response):
        response.cache_control.no_cache = True
        return response

    @app.bare_holster("/escape")
    @lift(no_cache)
    @app.holsterize
    def escape():
        return {}
