from werkzeug.datastructures import MIMEAccept

def preferring(mimetype, accept):
    """
    Rebuild a MIMEAccept to prefer a given mimetype.

    The given type will always appear at the front of the new header, causing
    it to be preferred.

    The preference is built by doubling the quality of the match with the
    given type.
    """

    types = []
    q = 2

    for name, value in accept:
        if name == mimetype:
            q = 2 * value
        else:
            types.append((name, value))

    return MIMEAccept([(mimetype, q)] + types)
