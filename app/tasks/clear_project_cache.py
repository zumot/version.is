import logging
from google.appengine.ext import webapp
from app.models import VersionCache


# Clear Cache Request Handler
class ClearCache(webapp.RequestHandler):
    def get(self, project):
        logging.info('Deleting tag cache from project: ' + project)
        for person in VersionCache.gql("WHERE project = :1", project):
            person.delete()
        logging.info('Deletion of ' + project + ' cache done.')
        self.response.write('Purged cache for: ' + project)


# Error catcher
class ClearCacheInvalidRequest(webapp.RequestHandler):
    def get(self):
        self.response.write('Invalid request. Specify project to purge...')
