import json
import yaml
import os.path

from collections import defaultdict
from google.appengine.ext import webapp
from google.appengine.api import urlfetch

from app.tasks.getversions import testHandler
from app.helpers import template

import logging


""" API URL to pull requests for the project registry
"""
def pullRequestApiUrl():
    return 'https://api.github.com/repos/version-is/version.is-sources/pulls'


""" parse yaml file
"""
def parseYamlFile(url):
    response = []
    # Get yaml file
    rawfile = urlfetch.fetch(url).content
    rawfile = yaml.load(rawfile)
    # Validate each yaml object
    for project in rawfile:
        data = defaultdict()

        data['project'] = project
        data['name'] = rawfile[project]['name']
        data['website'] = rawfile[project]['website']
        data['handler'] = rawfile[project]['handler']
        data['handler_valid'] = testHandler(data['handler']['type'])[0]

        response.append(data)

    return response


""" Parse the pull request contents
"""
def parsePullRequest(url):
    response = []
    # Get the list of files added in the pull request
    pullfiles = urlfetch.fetch(url + '/files')
    pullfiles = json.loads(pullfiles.content)
    for pullfile in pullfiles:
        pulldata = defaultdict()
        pulldata['filename'] = pullfile['filename']
        pulldata['status'] = pullfile['status']
        pulldata['patch'] = pullfile['patch']
        pulldata['raw_url'] = pullfile['raw_url']
        pulldata['blob_url'] = pullfile['blob_url']
        pulldata['extension'] = os.path.splitext(pullfile['filename'])[1][1:]
        if pulldata['extension'] == 'yaml':
            pulldata['valid'] = True
            pulldata['data'] = parseYamlFile(pullfile['raw_url'])
        else:
            pulldata['valid'] = False
            pulldata['data'] = {}

        response.append(pulldata)

    return response


""" Show a warning, if more than one file is changed
"""
def testFileCount(filecount):
    return filecount != 1


""" Get data about a pull request
"""
def getPullRequestData(data):
    # Build a dict with information about the pull request
    pulldata = defaultdict()

    # Get the pullreq number
    pulldata['number'] = data['number']
    # Get the link to the pull req
    pulldata['link'] = data['_links']['html']['href']
    # Get data about the files in the pull request
    pulldata['files'] = parsePullRequest(data['url'])
    # Bool: Is there more than one file?
    pulldata['file_count_warning'] = testFileCount(len(pulldata['files']))

    return pulldata


""" Get data about the open pull requests
"""
def getPullRequests():
    # Fetch the json object with all pull requests
    pullreqs = urlfetch.fetch(pullRequestApiUrl()).content
    pullreqs = json.loads(pullreqs)

    response = []

    # Get data for the open ones
    for pullreq in pullreqs:
        if pullreq['state'] == 'open':
            response.append(getPullRequestData(pullreq))

    return response


""" Request handler
"""
class ValidatePullReq(webapp.RequestHandler):
    def get(self):
        template_data = {
            'title': 'Pull Requests',
            'pullreqs': getPullRequests()  # Get data
        }

        rendered = template.render('validate_pullreq', template_data)

        self.response.write(rendered)  # Output the rendered data
