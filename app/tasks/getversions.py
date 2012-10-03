import json
import yaml
import logging
import time

from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.ext import webapp

from app.tasks import handlers
from app.models import FileCache
from app.models import Project

#
# Configuration
#
source_repo = 'gustavnikolaj/version.is-sources'


#
# Paths
#
raw_path = 'https://raw.github.com/' + source_repo + '/master/'
contents_path = 'https://api.github.com/repos/' + source_repo + '/contents'


#
# Test if a handler is indeed callable and from our handlers module
#
def testHandler(handler):
    handler_valid = True
    try:
        handler = getattr(handlers, handler)
    except AttributeError:
        handler_valid = False

    return (handler_valid, handler)


#
# Get list of files from repo
#
def getSourceFiles():
    repo_files = json.loads(urlfetch.fetch(contents_path).content)
    files = []
    for f in repo_files:
        if f['name'] != 'README.md':
            files.append((f['name'], f['sha']))

    return files


#
# Refresh cache or create
#
def fileCacheRefresh(f, sha):
    # Load yaml data from file.
    data = yaml.load(urlfetch.fetch(raw_path + f).content)

    # Format the data to be saved in the database
    data_json = json.dumps(data, separators=(',', ':'))

    # Attempt to load the record
    fc = FileCache.gql('WHERE project = :1', f).get()

    if fc:  # Save data to existing record
        fc.sha = sha
        fc.data = data_json
        fc.put()
    else:  # Create a new record
        fc = FileCache(filename=f, sha=sha, data=data_json)
        fc.put()

    return data


#
# Load projects from cache
#
def fileGet(f, sha):
    fc = FileCache.gql('WHERE filename = :1', f).get()

    if fc:
        if sha == fc.sha:
            logging.info('file unchanged, using cache.')
            return (False, json.loads(fc.data))
        else:
            logging.info('file changed, refreshing cache.')
            return (True, fileCacheRefresh(f, sha))
    else:
        logging.info('file not in cache, retrieving.')
        return (True, fileCacheRefresh(f, sha))


#
#
#
def projectGet(p, d, filename, refresh):
    # Refresh meta data about the project if needed
    if refresh:
        data = {
            'prettyname': d['name'],
            'website': d['website'],
            'handler': d['handler']['type']
        }
        data = json.dumps(data, separators=(',', ':'))
        pm = Project.gql('WHERE project = :1', p).get()
        if pm:
            pm.data = data
        else:
            pm = Project(project=p, data=data)
        pm.put()

    # Get version info with specified handler
    handler = d['handler']['type']
    handlerargs = d['handler']

    h = testHandler(handler)

    if h[0]:
        version = h[1](p, handlerargs)
        logging.info('current version: ' + version)
        # Cache version for an hour
        memcache.set('version:' + p, version, 3600)
    else:
        logging.error('invalid Handler!')


#
# Request handler object
#
class ImportVersionData(webapp.RequestHandler):
    def get(self):
        # Adjusting log format for more readable output
        log_format = "%(levelname)-8s %(asctime)s %(message)s"
        fr = logging.Formatter(log_format)
        logging.getLogger().handlers[0].setFormatter(fr)

        # Init logging messages
        logging.info('#' * 40)
        logging.info('#' * 40)
        logging.info('REFRESHING VERSION DATA...')
        logging.info('source repo: ' + source_repo)
        logging.info('#' * 40)

        # Set starting point for timing.
        start = time.time()

        # Read all files from source repo.
        for filename, sha in getSourceFiles():
            logging.info('#' * 40)
            logging.info('source: ' + filename)
            # Check all projects in each source file.
            projects = fileGet(filename, sha)
            projects_refreshed = projects[0]
            for p in projects[1]:
                logging.info('-' * 40)
                logging.info('checking "' + p + '"')
                projectGet(p, projects[1][p], filename, projects_refreshed)

        logging.info('#' * 40)

        # Calculate execution time.
        exectime = "{0:.3f}".format(time.time() - start)
        # Format execution time.
        response = 'Task finished in ' + str(exectime) + ' seconds.'
        # Log it.
        logging.info(response)
        # Print it. Reference to Log for details.
        self.response.write(response + ' Check logs for details.')
