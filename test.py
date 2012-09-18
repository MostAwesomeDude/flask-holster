from flask import Flask
from flask.ext.holster.main import holsterize

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
            "xss-sword": "<>"
        }
    }

if __name__ == "__main__":
    app.run()
