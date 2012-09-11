import webapp2
import json
import urllib2
from collections import defaultdict
import re
from google.appengine.api import memcache


gist_id = '3691351'


class GetVersions(webapp2.RequestHandler):
    def get(self):
        versions = defaultdict()

        self.response.headers['Content-Type'] = 'application/json'
        gist = urllib2.urlopen('https://api.github.com/gists/' + gist_id).read()
        gist = json.loads(gist)
        manual = json.loads(gist['files']['versions.json']['content'])
        dynamic = json.loads(gist['files']['sources.json']['content'])

        for key in manual:
            versions[key] = manual[key]

        for key in dynamic:
            filename = dynamic[key].split('/')[-1]
            if filename == 'package.json' or filename == 'component.json':
                content = urllib2.urlopen(dynamic[key]).read()
                content = json.loads(content)
                versions[key] = content['version']
            if filename == 'grunt.js':
                content = urllib2.urlopen(dynamic[key]).read()
                matches = re.search('version: \'(.*)\'', content)
                versions[key] = matches.group(1)

        memcache.add('versions', versions)


app = webapp2.WSGIApplication([
    webapp2.Route('/tasks/get-versions', GetVersions)
], debug=True)
