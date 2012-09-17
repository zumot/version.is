import json
import datetime
import hashlib
import logging
from google.appengine.ext import db
from google.appengine.api import urlfetch
from app.models import VersionCache


def firefox(project, data):
    url = 'http://people.mozilla.com/~tmielczarek/branch_versions.json'
    content = urlfetch.fetch(url).content
    project_data = json.loads(content)
    sha = hashlib.sha1()
    sha.update(content)
    sha = sha.hexdigest()

    q = db.GqlQuery("SELECT * FROM VersionCache WHERE project = :1 AND commit = :2", project, sha)

    if q.count() == 0:
        logging.info('refreshing ' + project + ' version data')

        version_version = project_data[data['key']]

        t = VersionCache(project=project,
                         version=version_version,
                         commit=sha,
                         date=datetime.datetime.now())
        t.put()
    else:
        logging.info('version data for ' + project + ' unchanged')

    q = db.GqlQuery("SELECT version FROM VersionCache WHERE project = :1 ORDER BY date DESC", project).get()
    return q.version
