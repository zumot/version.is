import json
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from app.tasks.getversions import testHandler


class ValidateProject(webapp.RequestHandler):
    def get(self):
        test_file = self.request.get('url')
        test = True

        if test_file == '':
            self.response.write('No url for test file given. Set it in ?url=')
        else:
            content = urlfetch.fetch(test_file)
            filename = test_file.split('/')[-1].replace('.json', '')

            # Test if the file exists at all.
            if not content.status_code == 200:
                test = False
                self.response.write('The file could not be found.')
            else:
                # Load content if it exists.
                content = json.loads(content.content)

            # Check if project name and file name is the same. They should be.
            if test:
                if not content['project'] == filename:
                    test = False
                    self.response.write('The name of the project and the name of the .json file does not match.')

            # Test if the specified handler exists.
            if test:
                if not testHandler(content['handler']['handler'])[0]:
                    test = False
                    self.response.write('The handler was either not specified or valid.')

            if test:
                self.response.write('Test passed')
