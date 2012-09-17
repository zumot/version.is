import json
import logging
import time
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from app.models import ShaCache, Project
from app.tasks import handlers


#
# Return the raw path for the project json file
#
def rawPath(project):
    return 'https://raw.github.com/gustavnikolaj/version.is-sources/master/' + project + '.json'


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
# Refresh cache of project
#
def refreshProjectCache(name, sha):
    # Delete old Project models for the project if they exists
        for p in Project.gql("WHERE project = :1", name):
            p.delete()

        # Delete old ShaCache models for the project if they exists
        for s in ShaCache.gql("WHERE project = :1", name):
            s.delete()

        # Fetch new data, loads and dumps json to remove newlines from the input. (multiline not ok in datastore)
        data = json.dumps(json.loads(urlfetch.fetch(rawPath(name)).content), separators=(',', ':'))

        # Put new project data into a Project Model
        p = Project(project=name, data=data)
        p.put()

        # Put new sha hash into a ShaCache Model
        s = ShaCache(project=name, sha=sha)
        s.put()


#
# Load project data
#
def loadProjectData(name):
    p = Project.gql("WHERE project = :1", name).get()
    return json.loads(p.data)


#
# Request Handler object called from /tasks.py
#
class ImportVersionData(webapp.RequestHandler):
    def get(self):
        logging.info('Checking versions...')
        start = time.time()  # Set starting point for timing.

        repo = "gustavnikolaj/version.is-sources"
        repo_url = "https://api.github.com/repos/" + repo + "/contents"

        repo_data = json.loads(urlfetch.fetch(repo_url).content)

        for project in repo_data:
            shacache_all = ShaCache.all()  # Have to be called on each loop, otherwise it will not reset the filters
            name = project['name'].replace('.json', '')

            if name != 'README.md':  # Dont try to do work with the README.md file :-)
                sha = project['sha']

                # If no cache record for the file exists, it means that it's either new or changed. Refresh!
                if shacache_all.filter('project =', name).filter('sha =', sha).count() == 0:
                    refreshProjectCache(name, sha)

                # Load data from cache...
                data = loadProjectData(name)

                # Check if the specified handler is indeed a valid handler.
                h = testHandler(data['handler']['handler'])

                # Log the response.
                if h[0]:
                    version = h[1](name, data['handler'])
                    logging.info('Current version of ' + data['project'] + ' is ' + version)
                    memcache.set('version:' + name, version)
                else:
                    logging.error('Could not get version info about ' + data['project'] + ': invalid handler specified.')

        exectime = "{0:.3f}".format(time.time() - start)  # Calculate execution time.
        response = 'Task finished in ' + str(exectime) + ' seconds.'  # Format execution time.
        logging.info(response)  # Log it.
        self.response.write(response + ' Check logs for details.')  # Print it. Reference to Log for details.
