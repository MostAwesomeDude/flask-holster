ext_dict = {
    "html": "text/html",
    "json": "application/json",
}

def guess_type(ext):
    """
    Guess which MIME type fits the given extension.
    """

    return ext_dict.get(ext, "text/plain")
