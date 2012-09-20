from flask import Flask
from flask.ext.holster.main import holsterize, with_template
from flask.ext.holster.views import HTMLTemplate

app = Flask(__name__)
holsterize(app)

app.debug = True

@app.holster("/test")
def test():
    from math import pi

    return {
        "data": "Hello from Holster!",
        "nested": {
            "numeric": 0,
            "floating": pi,
            "unicode": u"Espa\xf1ol",
        },
        "secure": {
            "xss-sword": ';!--"<XSS>=&{()}',
        }
    }

custom_template = """
<h1>{{ d.header }}</h1>
"""

@app.holster("/custom")
@with_template("html", HTMLTemplate(custom_template))
def custom():
    return {"header": "HELLO OUT THERE"}

if __name__ == "__main__":
    app.run()
