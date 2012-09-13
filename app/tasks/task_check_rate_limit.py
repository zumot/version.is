import json
import logging
from google.appengine.ext import webapp
from google.appengine.api import urlfetch


class RateCheck(webapp.RequestHandler):
    def get(self):
        url = 'https://api.github.com/rate_limit'
        rate = urlfetch.fetch(url).content
        rate = json.loads(rate)

        self.response.status = 200
        self.response.headers['Charset'] = 'utf-8'
        self.response.headers['Content-Type'] = 'text/plain'

        self.response.write('GitHub API status:\n---------------------\n')
        self.response.write('Limit:     ' + str(rate['rate']['limit']).rjust(10) + '\n')
        self.response.write('Remaining: ' + str(rate['rate']['remaining']).rjust(10))

        logging.info('GitHub API status: ' + str(rate['rate']['remaining']) + ' remaining of ' + str(rate['rate']['limit']) + ' limit')
