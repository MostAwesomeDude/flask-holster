from functools import wraps

def lift(f):
    """
    "Decoratorial" lift.

    This is a functorial map specialized over functions, and I could talk
    about the category theory behind it, but the main takeaway is that you can
    use this as a decorator to lift a function on data to a function between
    functions on that data.

    >>> def first(x):
    ...  return x + 1
    ...
    >>> def second(x):
    ...  return x * 2
    ...
    >>> def third(x):
    ...  return x ** 3
    ...
    >>> @lift(third)
    ... @lift(second)
    ... @lift(first)
    ... def const():
    ...  return 1
    ...
    >>> const()
    64
    """

    @wraps(f)
    def deco(g):
        @wraps(g)
        def inner(*args, **kwargs):
            return f(g(*args, **kwargs))
        return inner
    return deco
