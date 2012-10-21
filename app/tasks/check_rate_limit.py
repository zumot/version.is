import json

from google.appengine.ext import webapp
from google.appengine.api import urlfetch

from app.helpers import ghAuth


class RateCheck(webapp.RequestHandler):
    def get(self):
        url = ghAuth('https://api.github.com/rate_limit')
        rate = urlfetch.fetch(url).content
        rate = json.loads(rate)

        self.response.status = 200
        self.response.headers['Charset'] = 'utf-8'
        self.response.headers['Content-Type'] = 'text/plain'

        self.response.write('GitHub API status:\n---------------------\n')
        self.response.write('Limit:     ' + str(rate['rate']['limit']).rjust(10) + '\n')
        self.response.write('Remaining: ' + str(rate['rate']['remaining']).rjust(10))
