from google.appengine.api import memcache
from google.appengine.ext import webapp
from app.helpers import format, template
from google.appengine.ext import db
import json
from app.models import Project


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


def getVersion(project):
    v = memcache.get('version:' + project)
    if not v:
        q = db.GqlQuery("SELECT * FROM VersionCache WHERE project = :1 ORDER BY date DESC", project)
        if q.count() == 0:
            return False
        else:
            return q.get().version
    else:
        return v


def getVersionDetailed(project):
    version = getVersion(project)
    p = Project.all().filter('project = ', project).get()
    d = db.GqlQuery("SELECT date FROM VersionCache WHERE project = :1 ORDER BY date DESC", project).get()
    return (version, json.loads(p.data), d.date.date())


def projectHtml(project):
    version = getVersion(project)

    if version:
        version = getVersionDetailed(project)
        status = 200
        if version[1]['meta']['prettyname']:
            project = version[1]['meta']['prettyname']

        template_data = {
            'title': project,
            'project': project,
            'version': version[0],
            'meta': version[1]['meta'],
            'handler': version[1]['handler']['handler'],
            'date': version[2].isoformat()
        }
        result = template.render('response', template_data)
    else:
        status = 404
        template_data = {
            'title': 'Error!',
            'message': 'No data for ' + project
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

    if callback != '':
        content = json.dumps(content, separators=(',', ':'))
        content = callback + '(' + content + ');'
    else:
        content = json.dumps(content, indent=2)

    return (content, status)
