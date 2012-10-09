def match_with_wildcard(s1, s2):
    """
    If either parameter is the wildcard, match. Otherwise, check for equality.
    """

    if s1 == "*":
        return s2
    elif s2 == "*":
        return s1
    elif s1 == s2:
        return s1
    else:
        return None

class MIME(object):
    """
    A MIME type.
    """

    def __init__(self, category, filetype, q):
        self.category = category
        self.filetype = filetype
        self.params = {"q": q}

    def __str__(self):
        params = ", ".join("%s = %s" % t for t in self.params.iteritems())
        return "%s (%s)" % (self.plain(), params)

    __repr__ = __str__

    @classmethod
    def from_string(cls, s):
        pieces = s.split(";")
        category, filetype = pieces[0].split("/")
        self = cls(category, filetype, 1.0)

        for piece in pieces[1:]:
            if "=" in piece:
                k, v = piece.split("=", 1)
                # Special case for q.
                if k == "q":
                    v = float(v)
                self.params[k] = v

        return self

    def plain(self):
        return "%s/%s" % (self.category, self.filetype)

    def match(self, other):
        """
        Create a new MIME type representing the quality of the match between
        this type and the other type.
        """

        category = match_with_wildcard(self.category, other.category)
        filetype = match_with_wildcard(self.filetype, other.filetype)

        if category and filetype:
            return MIME(category, filetype, self.params["q"] *
                other.params["q"])
        else:
            return MIME("*", "*", 0.0)

class Accept(object):
    """
    The Accept header, as defined by RFC 2616.
    """

    def __init__(self, s):
        self.types = [MIME.from_string(x) for x in s.split(",")]

    def __str__(self):
        return "<Accept [%s]>" % ", ".join(str(x) for x in self.types)

    __repr__ = __str__

    def prefer(self, s):
        """
        Parse a MIME type and prefer it over the other types in this listing.
        """

        mime = MIME.from_string(s)
        for t in self.types:
            t.params["q"] *= 0.5
        self.types.append(mime)

    def match(self, other):
        """
        Generate a list of matched MIME types from another Accept listing.
        """

        # As long as we can't have itertools.product(), we have to do this the
        # slow way.
        l = []

        for x in self.types:
            for y in other.types:
                l.append(x.match(y))

        return l

    def best(self, other):
        """
        Given another Accept listing, choose the best acceptable MIME type.

        None will be returned if no acceptable type could be found.
        """

        l = self.match(other)
        l.sort(key=lambda mime: mime.params["q"], reverse=True)
        if l:
            return l[0]
        return None
