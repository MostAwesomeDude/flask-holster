"""
Oftentimes, one simply wants to get a common task done. This module faciliates
that in the context of Holster.
"""

from flask_holster.main import with_template
from flask_holster.views import HTMLTemplate

def html(template):
    """
    Render this holstered handler with the given template.

    The template is supposed to be a file path; think of this helper as
    replacing ``render_template()``.
    """

    return with_template("text/html", HTMLTemplate(template,
        from_string=False))
