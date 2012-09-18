from google.appengine.ext import webapp
from app.views.projects import Projects
from app.views.projectversion import ProjectVersion
from app.views.index import Index


app = webapp.WSGIApplication([
    webapp.Route('/', Index),
    webapp.Route('/projects', Projects),
    webapp.Route('/<project:[a-zA-Z0-9-_](.*)>', ProjectVersion)
], debug=True)
