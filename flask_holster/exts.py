ext_dict = {
    "html": "text/html",
    "json": "application/json",
    "svg":  "image/svg+xml",
    # The YAML MIME type is not standardized. This is the same type Rails
    # uses; hopefully it is close enough.
    "yaml": "application/x-yaml",
}

def guess_type(ext):
    """
    Guess which MIME type fits the given extension.
    """

    return ext_dict.get(ext, "text/plain")
