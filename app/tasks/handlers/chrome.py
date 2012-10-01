import json
import datetime
import hashlib
import logging
from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import memcache
from app.models import VersionCache


def chrome(project, data):
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
        logging.info(project + ': refreshing version data')

        for os in project_data:
            if os['os'] == data['os']:
                os_versions = os['versions']

        for vs in os_versions:
            if vs['channel'] == data['channel']:
                version_version = vs['version']
                version_date = datetime.datetime.strptime(vs['date'], "%m/%d/%y")

        t = VersionCache(project=project,
                         version=version_version,
                         commit=sha,
                         date=version_date)
        t.put()
    else:
        logging.info(project + ': version data for unchanged')

    q = db.GqlQuery("SELECT version FROM VersionCache WHERE project = :1 ORDER BY date DESC", project).get()
    return q.version
