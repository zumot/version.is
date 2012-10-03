from google.appengine.api import memcache
from google.appengine.ext import db


def getVersion(project):
    v = memcache.get('version:' + project)
    if not v:
        q = db.GqlQuery("SELECT * FROM VersionCache WHERE project = :1 ORDER BY date DESC", project)
        if q.count() == 0:
            return False
        else:
            v = q.get().version
            # Cache the data for for 10 minutes
            memcache.set('version:' + project, v, 600)
            return v
    else:
        return v
