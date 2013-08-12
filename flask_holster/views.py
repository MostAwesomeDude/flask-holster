from flask import json, render_template, render_template_string

default_html_template = """
<!DOCTYPE html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta charset="utf-8" />
    {% if d["title"] is defined %}
        <title>{{ d["title"] }}</title>
    {% endif %}
</head>
<body>
{% macro dump(d) %}
    <ul>
    {% for k in d %}
        {% set v = d[k] %}
        {% if v is defined %}
            <li>{{ k }}:
                {% if v is mapping %}
                <ul>{{ dump(v) }}</ul>
                {% else %}
                {{ v|e }}
                {% endif %}
            </li>
        {% else %}
            <li>{{ k }}</li>
        {% endif %}
    {% endfor %}
    </ul>
{% endmacro %}
{{ dump(d) }}
</body>
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


class BetterJSONEncoder(json.JSONEncoder):

    def default(self, o):
        try:
            return o.__json__()
        except AttributeError:
            return super(BetterJSONEncoder, self).default(o)


class JSONRenderer(object):

    def format(self, d):
        return BetterJSONEncoder().encode(d)


class YAMLRenderer(object):

    def format(self, d):
        """
        Serialize a dictionary into YAML.

        Format using PyYAML's yaml module if available, or json otherwise.
        This is fine, because JSON is a subset of YAML.
        """

        try:
            from yaml import safe_dump
            return safe_dump(d)
        except ImportError:
            return JSONRenderer().format(d)


class Str(object):

    def format(self, d):
        return str(d)


templates = {
    "application/json":   JSONRenderer(),
    "application/x-yaml": YAMLRenderer(),
    "text/html":          HTMLTemplate(),
    "text/plain":         Str(),
}
