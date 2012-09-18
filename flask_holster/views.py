from flask import json, render_template_string

html_template = """
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

    def format(self, d):
        return render_template_string(html_template, d=d)



class JSONTemplate(object):

    def format(self, d):
        return json.dumps(d)



class PlainTemplate(object):

    def format(self, d):
        return str(d)



templates = {
    "text/html":        HTMLTemplate,
    "application/json": JSONTemplate,
    "text/plain":       PlainTemplate,
}
