from flask import Flask
from flask.ext.holster.main import init_holster, with_template
from flask.ext.holster.views import HTMLTemplate

app = Flask(__name__)
init_holster(app)

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

@app.holster("/<int:i>/param")
def param(i):
    return {"parameter": i}

@app.holster("/multiple/<int:i>/<int:j>")
@app.holster("/multiple/<int:i>")
@app.holster("/multiple")
def multiple(i=None, j=None):
    return {"first": i, "second": j}

if __name__ == "__main__":
    app.run()
