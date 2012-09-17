import json

from google.appengine.ext import webapp
from app.helpers import format, template

from app.views.projects import projectsListDetailed


class Index(webapp.RequestHandler):
    def get(self):
        response_format = format.get(self.request.get('format'), self.request.headers['accept'])

        response = gimmeIndex(response_format, self.request.get('callback'))

        self.response.status = response[1]
        self.response.headers['Charset'] = 'utf-8'
        self.response.headers['Content-Type'] = response_format

        self.response.write(response[0])


def gimmeIndex(response_format, callback):
    formats = format.formats()

    if response_format == formats[0]:
        return indexHtml()
    if response_format == formats[1]:
        return indexPlain()
    if response_format == formats[2]:
        return indexJson(callback)


def indexHtml():
    template_data = {'projects': projectsListDetailed()}
    return (template.render('index', template_data), 200)


def indexPlain():
    return ('Invalid request', 400)


def indexJson(callback):
    content = {'message': 'Invalid Request'}

    if callback != '':
        content = json.dumps(content, separators=(',', ':'))
        content = callback + '(' + content + ');'
    else:
        content = json.dumps(content, indent=2)

    return (content, 400)
