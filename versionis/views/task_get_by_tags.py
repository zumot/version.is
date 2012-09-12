import json
import logging
import re
from collections import defaultdict
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.ext import db
from versionis.helpers import iso8601date
from versionis.models.version import Version


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

                    version_date = iso8601date.parse_iso8601_datetime(commit['commit']['author']['date'])  # Parse the date to python datetime
                    version_version = re.sub('^v(?=\d)', '', tag['name'])  # Remove leading v from version number

                    v = Version(project=project,
                                version=version_version,
                                commit=tag['commit']['sha'],
                                date=version_date)
                    v.put()
                    logging.info('added new version to ' + project + ': ' + version_version)

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
