from google.appengine.ext import webapp
from google.appengine.api import memcache
import json


charset = 'utf-8'


def projectsList():
    return memcache.get('versions')


class PlainProjects(webapp.RequestHandler):
    def get(self):
        self.response.status = 200
        self.response.headers['Charset'] = charset
        self.response.headers['Content-Type'] = 'text/plain'

        projects = projectsList()

        if projects:
            for project in projects:
                self.response.write(project + ': ' + projects[project] + "\n")
        else:
            self.response.write('No projects is monitored at the moment.')


class JsonProjects(webapp.RequestHandler):
    def get(self):
        self.response.status = 200
        self.response.headers['Charset'] = charset
        self.response.headers['Content-Type'] = 'application/json'

        projects = projectsList()

        if projects:
            content = projects
        else:
            content = {'error': 'No projects is monitored at the moment.'}

        callback = self.request.get('callback')

        if callback != '':
            content = json.dumps(content, separators=(',', ':'))
            self.response.write(callback + '(' + content + ');')
        else:
            content = json.dumps(content, indent=2)
            self.response.write(content)


app = webapp.WSGIApplication([
    webapp.Route('/projects/json', JsonProjects),
    webapp.Route('/projects', PlainProjects)
], debug=True)
