import json
import logging
import re
from google.appengine.api import urlfetch
from google.appengine.ext import db
from app.helpers import iso8601date
from app.models import VersionCache


def bytags(project, data):
    repo = data['source']

    # Loading tags for current project
    tags_url = 'https://api.github.com/repos/' + repo + '/tags'
    tags = json.loads(urlfetch.fetch(tags_url).content)

    refresh = False

    # Looping over tags
    for tag in tags:
        # If tags are not in the database, add them
        q = db.GqlQuery("SELECT * FROM VersionCache WHERE project = :1 AND commit = :2", project, tag['commit']['sha'])
        if (q.count() == 0):
            refresh = True
            commit_url = 'https://api.github.com/repos/' + repo + '/commits/' + tag['commit']['sha']
            commit = json.loads(urlfetch.fetch(commit_url).content)

            version_date = iso8601date.parse_iso8601_datetime(commit['commit']['author']['date'])  # Parse the date to python datetime
            version_version = re.sub('^v(?=\d)', '', tag['name'])  # Remove leading v from version number

            t = VersionCache(project=project,
                             version=version_version,
                             commit=tag['commit']['sha'],
                             date=version_date)
            t.put()

    if refresh:
        logging.info('refreshed ' + project + ' version data')
    else:
        logging.info('version data for ' + project + ' unchanged')

    # Return the most recent released version
    q = db.GqlQuery("SELECT version FROM VersionCache WHERE project = :1 ORDER BY date DESC", project).get()
    return q.version
