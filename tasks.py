from google.appengine.ext import webapp
from app.tasks.get_by_tags import ImportVersions
from app.tasks.clear_project_cache import ClearCache, ClearCacheInvalidRequest
from app.tasks.check_rate_limit import RateCheck


app = webapp.WSGIApplication([
    webapp.Route('/tasks/get-tags', ImportVersions),
    webapp.Route('/tasks/clear-cache', ClearCacheInvalidRequest),
    webapp.Route('/tasks/clear-cache/<project:[a-z0-9-_](.*)>', ClearCache),
    webapp.Route('/tasks/check-rate-limit', RateCheck)
], debug=True)
