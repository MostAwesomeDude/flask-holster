from flask import json

class JSONTemplate(object):

    def format(self, d):
        return json.dumps(d)



class PlainTemplate(object):

    def format(self, d):
        return str(d)



templates = {
    "application/json": JSONTemplate,
    "text/plain":       PlainTemplate,
}
