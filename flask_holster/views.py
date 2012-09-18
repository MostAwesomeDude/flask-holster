from flask import json, render_template_string

html_template = """
<ul>
{% for k in d recursive %}
    {% set v = d[k] %}
    {{ d|pprint }}
    <li>{{ k }}:
        {% if v is mapping %}
        <ul>{{ loop(v) }}</ul>
        {% else %}
        {{ v }}
        {% endif %}
    </li>
{% endfor %}
</ul>
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
