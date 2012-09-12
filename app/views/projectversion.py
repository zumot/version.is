from google.appengine.api import memcache
from google.appengine.ext import webapp
from app.helpers import format
import json


class ProjectVersion(webapp.RequestHandler):
    def get(self, project):
        response_format = format.get(self.request.get('format'), self.request.headers['accept'])

        response = gimmeProject(project, response_format, self.request.get('callback'))

        self.response.status = response[1]
        self.response.headers['Charset'] = 'utf-8'
        self.response.headers['Content-Type'] = response_format

        self.response.write(response[0])


def gimmeProject(project, response_format, callback):
    formats = format.formats()

    if response_format == formats[0]:
        return projectHtml(project)
    if response_format == formats[1]:
        return projectPlain(project)
    if response_format == formats[2]:
        return projectJson(project, callback)


def projectHtml(project):
    array = memcache.get('versions')

    if project in array:
        status = 200
        result = '<p>Version of ' + project + ' is:</p><h1>' + array[project] + '</h1>'
    else:
        status = 404
        result = '<p>No data for ' + project + '</p>'

    return (result, status)


def projectPlain(project):
    array = memcache.get('versions')

    if project in array:
        status = 200
        result = array[project]
    else:
        status = 404
        result = 'No data for ' + project

    return (result, status)


def projectJson(project, callback):
    array = memcache.get('versions')

    if project in array:
        status = 200
        content = {'project': project, 'version': array[project]}
    else:
        status = 404
        content = {'error': 'No data for ' + project}

    if callback != '':
        content = json.dumps(content, separators=(',', ':'))
        content = callback + '(' + content + ');'
    else:
        content = json.dumps(content, indent=2)

    return (content, status)
