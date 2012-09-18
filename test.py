from flask import Flask
from flask.ext.holster.main import holsterize

app = Flask(__name__)
holsterize(app)

@app.holster("/test")
def test():
    return {"data": "Hello from Holster!"}

if __name__ == "__main__":
    app.run()
