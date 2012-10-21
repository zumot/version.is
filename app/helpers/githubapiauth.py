from google.appengine.api import memcache

import logging


""" Authentication with the GitHub API

For unauthenticated requests, there is currently a limit of 60 requests 
per hour. I have only experienced hitting that when doing a full refresh
or in testing.


It is, although an edge case, possible to hit this in a production setting.
Therefore I've added this.

If client_id and client_secret is set in memcache, this will return a 
querystring containing those two. Otherwise it will return an empty string.
This ensures that even though it cannot authenticate, it will continue
working under most circumstances.
"""

# Global vars
auth_data_fetched = False
client_id = ''
client_secret = ''


# Load from memcache
def loadAuthData():
	global auth_data_fetched, client_id, client_secret
	auth_data_fetched = True
	client_id = memcache.get('github_oauth_client_id')
	client_secret = memcache.get('github_oauth_client_secret')


def ghAuthQs():
	# If they are both set
	if client_id and client_secret:
		return '?client_id=' + client_id + '&client_secret=' + client_secret
	else:
		# If we have tried to fetch it and they were not set continue without validation
		if auth_data_fetched:
			return ''
		else:
			loadAuthData()  # Attempt to load the data
			return ghAuthQs()  # Run this function again

def ghAuth(url):
	return url + ghAuthQs()
