import json
import logging
import re
from google.appengine.api import urlfetch
from google.appengine.ext import db
from app.helpers import iso8601date
from app.models import VersionCache
from app.helpers import ghAuth


def bytags(p, data):
    repo = data['repo']

    # Loading tags for current project
    tags_url = ghAuth('https://api.github.com/repos/' + repo + '/tags')
    tags = json.loads(urlfetch.fetch(tags_url).content)

    refresh = False

    # Looping over tags
    for tag in tags:
        # If tags are not in the database, add them
        query = "SELECT * FROM VersionCache WHERE project = :1 AND commit = :2"
        q = db.GqlQuery(query, p, tag['commit']['sha'])
        if (q.count() == 0):
            refresh = True
            commit_url = ghAuth(
                'https://api.github.com/repos/' + repo +
                '/commits/' + tag['commit']['sha']
            )
            commit = json.loads(urlfetch.fetch(commit_url).content)

            # Parse the date to python datetime
            version_date = commit['commit']['author']['date']
            version_date = iso8601date.parse_iso8601_datetime(version_date)
            # Remove leading v from version number if present
            version_version = re.sub('^v(?=\d)', '', tag['name'])

            t = VersionCache(project=p,
                             version=version_version,
                             commit=tag['commit']['sha'],
                             date=version_date)
            t.put()

    if refresh:
        logging.info('refreshed version data')
    else:
        logging.info('version data unchanged')

    # Return the most recent released version
    query = (
        "SELECT version FROM VersionCache WHERE project = :1 " +
        "ORDER BY date DESC"
    )
    q = db.GqlQuery(query, p).get()
    return q.version
