import json
import logging
from datetime import datetime, timedelta
from collections import defaultdict
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.ext import db


# Version database model
class Version(db.Model):
    project = db.StringProperty(required=True)
    version = db.StringProperty(required=True)
    commit = db.StringProperty(required=True)
    date = db.DateTimeProperty(required=True)


# ISO8601 date string to datetime parser
def parse_iso8601_datetime(dtstr, loose=False):
    """
    Convert ISO8601 datetime string and return Python datetime.datetime.
    Specify loose=True for more relaxed parsing accepting eg "YYYY-MM-DD" format.

    Raise ValueError on malformed input.
    reference: http://stackoverflow.com/questions/8569396/storing-rss-pubdate-in-app-engine-datastore#answer-8570029
    """
    dt = None
    if len(dtstr) == 19:    # (eg '2010-05-07T23:12:51')
        dt = datetime.strptime(dtstr, "%Y-%m-%dT%H:%M:%S")
    elif len(dtstr) == 20:  # (eg '2010-05-07T23:12:51Z')
        dt = datetime.strptime(dtstr, "%Y-%m-%dT%H:%M:%SZ")
    elif len(dtstr) == 25:  # (eg '2010-05-07T23:12:51-08:00')
        dt = datetime.strptime(dtstr[0:19], "%Y-%m-%dT%H:%M:%S")
        tzofs = int(dtstr[19:22])
        dt = dt - timedelta(hours=tzofs)
    else:
        if loose:
            if len(dtstr) == 10:  # (eg '2010-05-07')
                dt = datetime.strptime(dtstr, "%Y-%m-%d")
        if not dt:
            raise ValueError("Invalid ISO8601 format: '%s'" % dtstr)
    return dt


# Request Handler and Processing object
class ImportVersions(webapp.RequestHandler):
    def get(self):
        logging.info('Calculating new versions list from tags')

        gist_id = '3697931'  # ref https://gist.github.com/3697931

        versions = defaultdict()  # Dict object to store project versions

        # Get list of projects to monitor
        gist = urlfetch.fetch('https://api.github.com/gists/' + gist_id).content
        gist = json.loads(gist)
        repos = json.loads(gist['files']['projects.json']['content'])

        # Loop over projects...
        for project in repos:
            # Loading tags for current project
            tags_url = 'https://api.github.com/repos/' + repos[project] + '/tags'
            logging.info('getting ' + project + ' tags')
            tags = json.loads(urlfetch.fetch(tags_url).content)

            # Looping over tags
            for tag in tags:
                # If tags are not in the database, add them
                q = db.GqlQuery("SELECT * FROM Version WHERE project = :1 AND commit = :2", project, tag['commit']['sha'])
                if (q.count() == 0):
                    commit_url = 'https://api.github.com/repos/' + repos[project] + '/commits/' + tag['commit']['sha']
                    commit = json.loads(urlfetch.fetch(commit_url).content)

                    v = Version(project=project,
                                version=tag['name'],
                                commit=tag['commit']['sha'],
                                date=parse_iso8601_datetime(commit['commit']['author']['date']))
                    v.put()
                    logging.info('added new version to ' + project + ': ' + tag['name'])

            # Add most recent (by date) version to version list
            q = db.GqlQuery("SELECT version FROM Version WHERE project = :1 ORDER BY date DESC", project).get()
            versions[project] = q.version

        # Add new versions list to memcache
        memcache.set('versions', versions)
        logging.info('Generated new versions list from tags')
        logging.info('Saved new versions list to memcache')


# Set up routing
app = webapp.WSGIApplication([
    webapp.Route('/tasks/get-tags', ImportVersions)
], debug=True)
