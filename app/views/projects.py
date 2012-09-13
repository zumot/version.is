from google.appengine.ext import webapp
from google.appengine.api import memcache
from app.helpers import format, template
import json


class Projects(webapp.RequestHandler):
    def get(self):
        response_format = format.get(self.request.get('format'), self.request.headers['accept'])

        self.response.status = 200
        self.response.headers['Charset'] = 'utf-8'
        self.response.headers['Content-Type'] = response_format

        self.response.write(gimmeProjects(response_format, self.request.get('callback')))


def projectsList():
    return memcache.get('versions')


def gimmeProjects(response_format, callback):
    formats = format.formats()

    if response_format == formats[0]:
        return projectsHtml()
    if response_format == formats[1]:
        return projectsPlain()
    if response_format == formats[2]:
        return projectsJson(callback)


def projectsHtml():
    template_data = {'projects': memcache.get('versions')}
    return template.render('projects', template_data)


def projectsPlain():
    projects = projectsList()

    if projects:
        result = ''
        for project in projects:
            result = result + project + ': ' + projects[project] + "\n"
    else:
        result = 'No projects is monitored at the moment.'

    return result


def projectsJson(callback):
    projects = projectsList()

    if projects:
        content = projects
    else:
        content = {'error': 'No projects is monitored at the moment.'}

    if callback != '':
        content = json.dumps(content, separators=(',', ':'))
        content = callback + '(' + content + ');'
    else:
        content = json.dumps(content, indent=2)

    return content
