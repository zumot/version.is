from google.appengine.ext import webapp

from app.helpers import format, template, jsonOutput
from app.helpers import getVersion, getVersionDetailed


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
    version = getVersion(project)

    if version:
        version = getVersionDetailed(project)
        status = 200
        if version[1]['prettyname']:
            project = version[1]['prettyname']

        date = None
        if version[2] != None:
            date = version[2].isoformat()

        template_data = {
            'title': project,
            'project': project,
            'version': version[0],
            'prettyname': version[1]['prettyname'],
            'website': version[1]['website'],
            'handler': version[1]['handler'],
            'date': date
        }
        result = template.render('response', template_data)
    else:
        status = 404
        template_data = {
            'title': 'Error 404',
            'message': 'No data for ' + project + '.'
        }
        result = template.render('error', template_data)

    return (result, status)


def projectPlain(project):
    version = getVersion(project)

    if version:
        status = 200
        result = version
    else:
        status = 404
        result = 'No data for ' + project

    return (result, status)


def projectJson(project, callback):
    version = getVersion(project)

    if version:
        status = 200
        content = {'project': project, 'version': version}
    else:
        status = 404
        content = {'error': 'No data for ' + project}

    content = jsonOutput(content, callback)

    return (content, status)
