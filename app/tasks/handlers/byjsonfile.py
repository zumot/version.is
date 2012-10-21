import json
import base64
import datetime
import logging
from google.appengine.ext import db
from google.appengine.api import urlfetch
from app.models import VersionCache
from app.helpers import ghAuth


def byjsonfile(project, data):
    repo = data['repo']
    filename = data['file']

    url = ghAuth('https://api.github.com/repos/' + repo + '/contents/' + filename)
    project_data = json.loads(urlfetch.fetch(url).content)

    sha = project_data['sha']
    q = db.GqlQuery("SELECT * FROM VersionCache WHERE project = :1 AND commit = :2", project, sha)

    if q.count() == 0:
        logging.info('refreshing version data')
        version_version = json.loads(base64.b64decode(project_data['content']))['version']

        t = VersionCache(project=project,
                         version=version_version,
                         commit=sha,
                         date=datetime.datetime.now())
        t.put()
    else:
        logging.info('version data unchanged')

    q = db.GqlQuery("SELECT version FROM VersionCache WHERE project = :1 ORDER BY date DESC", project).get()
    return q.version
