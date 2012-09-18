class MIME(object):
    """
    A MIME type.
    """

    def __init__(self, s):
        pieces = s.split(";")
        self.media = pieces[0]
        self.params = {}
        for piece in pieces[1:]:
            if "=" in piece:
                k, v = piece.split("=", 1)
                self.params[k] = v

    def __str__(self):
        if self.params:
            params = ", ".join("%s = %s" % t for t in self.params.iteritems())
            return "%s (%s)" % (self.media, params)
        return self.media

    __repr__ = __str__

class Accept(object):
    """
    The Accept header, as defined by RFC 2616.
    """

    def __init__(self, s):
        self.types = [MIME(x) for x in s.split(",")]

    def __str__(self):
        return "<Accept [%s]>" % ", ".join(str(x) for x in self.types)

    __repr__ = __str__
