import logging
from google.appengine.ext import webapp
from google.appengine.ext import db


# Version database model
class Version(db.Model):
    project = db.StringProperty(required=True)
    version = db.StringProperty(required=True)
    commit = db.StringProperty(required=True)
    date = db.DateTimeProperty(required=True)


# Clear Cache Request Handler
class ClearCache(webapp.RequestHandler):
    def get(self, project):
        logging.info('Deleting tag cache from project: ' + project)
        for person in Version.gql("WHERE project = :1", project):
            person.delete()
        logging.info('Deletion of ' + project + ' tag cache done.')
        self.response.write('Purged tag cache for: ' + project)


# Error catcher
class InvalidRequest(webapp.RequestHandler):
    def get(self):
        self.response.write('Invalid request. Specify project to purge...')


# Routing
app = webapp.WSGIApplication([
    webapp.Route('/tasks/clear-cache', InvalidRequest),
    webapp.Route('/tasks/clear-cache/<project:[a-z0-9-_](.*)>', ClearCache)
], debug=True)
