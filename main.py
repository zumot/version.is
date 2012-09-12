from google.appengine.ext import webapp
from versionis.views.projects import Projects
from versionis.views.projectversion import ProjectVersion


charset = 'utf-8'


class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Charset'] = charset
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.status = 400
        self.response.write('Invalid request')


app = webapp.WSGIApplication([
    webapp.Route('/', MainPage),
    webapp.Route('/projects', Projects),
    webapp.Route('/<project:[a-z0-9-_](.*)>', ProjectVersion)
], debug=True)
