from google.appengine.ext import webapp
from app.tasks.getversions import ImportVersionData
from app.tasks.clear_project_cache import ClearCache, ClearCacheInvalidRequest
from app.tasks.check_rate_limit import RateCheck
from app.tasks.validate_pullreq import ValidatePullReq


app = webapp.WSGIApplication([
    webapp.Route('/tasks/get-versions', ImportVersionData),
    webapp.Route('/tasks/clear-cache', ClearCacheInvalidRequest),
    webapp.Route('/tasks/clear-cache/<project:[a-z0-9-_](.*)>', ClearCache),
    webapp.Route('/tasks/check-rate-limit', RateCheck),
    webapp.Route('/tasks/pullreqs', ValidatePullReq)
], debug=True)
