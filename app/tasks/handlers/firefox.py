import json
import datetime
import hashlib
import logging
from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import memcache
from app.models import VersionCache


def firefox(project, data):
    url = data['source']
    content = memcache.get('cache:' + url)

    if content is None:
        content = urlfetch.fetch(url).content
        memcache.add('cache:' + url, content, 120)

    project_data = json.loads(content)

    sha = hashlib.sha1()
    sha.update(content)
    sha = sha.hexdigest()

    q = db.GqlQuery("SELECT * FROM VersionCache WHERE project = :1 AND commit = :2", project, sha)

    if q.count() == 0:
        logging.info('refreshing version data')

        version_version = project_data[data['branch']]

        t = VersionCache(project=project,
                         version=version_version,
                         commit=sha,
                         date=datetime.datetime.now())
        t.put()
    else:
        logging.info('version data unchanged')

    q = db.GqlQuery("SELECT version FROM VersionCache WHERE project = :1 ORDER BY date DESC", project).get()
    return q.version
