import json
import re
import logging
from collections import defaultdict
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.api import urlfetch


class ImportVersions(webapp.RequestHandler):
    def get(self):
        logging.info('Calculating new versions list')

        gist_id = '3691351'

        versions = defaultdict()

        gist = urlfetch.fetch('https://api.github.com/gists/' + gist_id).content
        gist = json.loads(gist)
        manual = json.loads(gist['files']['versions.json']['content'])
        dynamic = json.loads(gist['files']['sources.json']['content'])

        for key in manual:
            versions[key] = manual[key]

        for key in dynamic:
            filename = dynamic[key].split('/')[-1]
            if filename == 'package.json' or filename == 'component.json':
                content = urlfetch.fetch(dynamic[key]).content
                content = json.loads(content)
                versions[key] = content['version']
            if filename == 'grunt.js':
                content = urlfetch.fetch(dynamic[key]).content
                matches = re.search('version: \'(.*)\'', content)
                versions[key] = matches.group(1)

        self.response.write("Success")

        memcache.add('versions', versions)
        logging.info('Generated new versions list')
        logging.info('Saved new versions list to memcache')


app = webapp.WSGIApplication([
    webapp.Route('/tasks/get-versions', ImportVersions)
], debug=True)
