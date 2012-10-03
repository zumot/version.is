from google.appengine.ext import webapp

from app.helpers import format, template, jsonOutput
from app.helpers.getprojectslist import getProjectsList
from app.helpers.getprojectslist import getProjectsListDetailed


class Projects(webapp.RequestHandler):
    def get(self):
        resp_format = format.get(
            self.request.get('format'),
            self.request.headers['accept']
        )

        self.response.status = 200
        self.response.headers['Charset'] = 'utf-8'
        self.response.headers['Content-Type'] = resp_format

        resp = gimmeProjects(resp_format, self.request.get('callback'))

        self.response.write(resp)


def gimmeProjects(response_format, callback):
    formats = format.formats()

    if response_format == formats[0]:
        return projectsHtml()
    if response_format == formats[1]:
        return projectsPlain()
    if response_format == formats[2]:
        return projectsJson(callback)


def projectsHtml():
    template_data = {'projects': getProjectsListDetailed()}
    return template.render('projects', template_data)


def projectsPlain():
    projects = getProjectsList()

    if projects:
        result = ''
        for project in projects:
            result = result + project + "\n"
    else:
        result = 'No projects is monitored at the moment.'

    return result


def projectsJson(callback):
    projects = getProjectsList()

    if projects:
        content = projects
    else:
        content = {'error': 'No projects is monitored at the moment.'}

    return jsonOutput(content, callback)
