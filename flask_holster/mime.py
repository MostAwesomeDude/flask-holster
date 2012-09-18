def match_with_wildcard(s1, s2):
    """
    If either parameter is the wildcard, match. Otherwise, check for equality.
    """

    if s1 == "*" or s2 == "*":
        return True
    return s1 == s2

class MIME(object):
    """
    A MIME type.
    """

    def __init__(self, s):
        pieces = s.split(";")
        self.category, self.filetype = pieces[0].split("/")
        self.params = {"q": 1.0}
        for piece in pieces[1:]:
            if "=" in piece:
                k, v = piece.split("=", 1)
                # Special case for q.
                if k == "q":
                    v = float(v)
                self.params[k] = v

    def __str__(self):
        params = ", ".join("%s = %s" % t for t in self.params.iteritems())
        return "%s (%s)" % (self.plain(), params)

    __repr__ = __str__

    def plain(self):
        return "%s/%s" % (self.category, self.filetype)

    def match(self, s):
        """
        Return a quality parameter, as a float, indicating how well this type
        matches the given type string.

        0 indicates no match.
        """

        category, filetype = s.split("/")

        if category == "*":
            category = self.category
        if filetype == "*":
            filetype = self.filetype
        if (match_with_wildcard(category, self.category) and
            match_with_wildcard(filetype, self.filetype)):
            unified = "%s/%s" % (category, filetype)
            return unified, self.params["q"]
        else:
            return None, 0.0

class Accept(object):
    """
    The Accept header, as defined by RFC 2616.
    """

    def __init__(self, s):
        self.types = [MIME(x) for x in s.split(",")]

    def __str__(self):
        return "<Accept [%s]>" % ", ".join(str(x) for x in self.types)

    __repr__ = __str__

    def best(self, s):
        """
        Given a preferred MIME type as a string, return the best acceptable
        MIME type.

        None will be returned if no acceptable type could be found.
        """

        champ = None, 0.0
        for mime in self.types:
            t = mime.match(s)
            if t[1] > champ[1]:
                champ = t

        return champ[0]
