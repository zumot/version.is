import webapp2
import json
from google.appengine.api import memcache


charset = 'utf-8'


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Charset'] = charset
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.status = 400
        self.response.write('Invalid request')


class ProjectVersion(webapp2.RequestHandler):
    def get(self, project):
        array = memcache.get('versions')

        self.response.headers['Charset'] = charset
        self.response.headers['Content-Type'] = 'text/plain'

        if project in array:
            self.response.status = 200
            self.response.write(array[project])
        else:
            self.response.status = 404
            self.response.write('No data for ' + project)


class JsonProjectVersion(webapp2.RequestHandler):
    def get(self, project):
        array = memcache.get('versions')

        self.response.headers['Charset'] = charset
        self.response.headers['Content-Type'] = 'application/json'

        if project in array:
            self.response.status = 200
            content = {'project': project, 'version': array[project]}
        else:
            self.response.status = 404
            content = {'error': 'No data for ' + project}

        callback = self.request.get('callback')

        if callback != '':
            content = json.dumps(content, separators=(',', ':'))
            self.response.write(callback + '(' + content + ');')
        else:
            content = json.dumps(content, indent=2)
            self.response.write(content)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainPage),
    webapp2.Route('/<project:\w+>/json', JsonProjectVersion),
    webapp2.Route('/<project:\w+>', ProjectVersion)
], debug=True)
