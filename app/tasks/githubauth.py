from google.appengine.ext import webapp
from google.appengine.api import memcache


#
# Request handler object
#
class GitHubAuth(webapp.RequestHandler):
    def get(self):
		if memcache.get('github_oauth_client_id') and memcache.get('github_oauth_client_secret'):
			self.response.write('<p>Got Credentials</p>')
		self.response.write('<form action="/tasks/githubauth" method="post">')
		self.response.write('<p>')
		self.response.write('<input type="text" name="client_id" placeholder="Client ID">')
		self.response.write('</p>')
		self.response.write('<p>')
		self.response.write('<input type="text" name="client_secret" placeholder="Client Secret">')
		self.response.write('</p>')
		self.response.write('<p>')
		self.response.write('<input type="submit" name="submit" value="Set">')
		self.response.write('</p>')
		self.response.write('</form>')

    def post(self):
    	if self.request.get('submit') == 'Set':
    		if self.request.get('client_id') and self.request.get('client_secret'):
    			memcache.set('github_oauth_client_id', self.request.get('client_id'))
    			memcache.set('github_oauth_client_secret', self.request.get('client_secret'))
    			self.response.write('New credentials saved.')
    		else:
    			memcache.delete('github_oauth_client_id')
    			memcache.delete('github_oauth_client_secret')
    			self.response.write('Credentials deleted.')
