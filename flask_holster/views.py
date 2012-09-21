from flask import json, render_template, render_template_string

default_html_template = """
{% macro dump(d) %}
    <ul>
    {% for k in d %}
        {% set v = d[k] %}
        <li>{{ k }}:
            {% if v is mapping %}
            <ul>{{ dump(v) }}</ul>
            {% else %}
            {{ v|e }}
            {% endif %}
        </li>
    {% endfor %}
    </ul>
{% endmacro %}
{{ dump(d) }}
"""


class HTMLTemplate(object):

    def __init__(self, template=None, from_string=True):
        self.template = template if template else default_html_template
        self.from_string = from_string

    def format(self, d):
        if self.from_string:
            return render_template_string(self.template, d=d)
        else:
            return render_template(self.template, d=d)



class JSONTemplate(object):

    def format(self, d):
        return json.dumps(d)



class PlainTemplate(object):

    def format(self, d):
        return str(d)



templates = {
    "text/html":        HTMLTemplate(),
    "application/json": JSONTemplate(),
    "text/plain":       PlainTemplate(),
}

# YAML. Requires the yaml module to be installed.
try:
    from yaml import safe_dump

    class YAMLTemplate(object):

        def format(self, d):
            return safe_dump(d)

    templates["application/x-yaml"] = YAMLTemplate()
except ImportError:
    pass
