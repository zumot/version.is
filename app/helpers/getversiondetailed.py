from google.appengine.api import memcache
from google.appengine.ext import db

from app.models import Project

from getversion import getVersion

import json
import logging


def getVersionDetailed(project):
    v = getVersion(project)
    p = getProjectMeta(project)
    if p['handler'] == 'bytags':
        d = getProjectDate(project)
    else:
        d = None

    logging.info(p)

    return (v, p, d)


def getProjectMeta(project):
    p = memcache.get('version:' + project + ':meta')
    if not p:
        pd = Project.all().filter('project = ', project).get()
        p = json.loads(pd.data)
        memcache.set('version:' + project + ':meta', p, 600)

    return p


def getProjectDate(project):
    d = memcache.get('version:' + project + ':date')
    if not d:
        dq = "SELECT date FROM VersionCache WHERE project = :1 ORDER BY date DESC"
        dd = db.GqlQuery(dq, project).get()
        d = dd.date.date()
        memcache.set('version:' + project + ':date', d, 600)

    return d
