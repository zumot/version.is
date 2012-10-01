from google.appengine.ext import db


# File Cache Model
class FileCache(db.Model):
    filename = db.StringProperty(required=True)
    sha = db.StringProperty(required=True)
    data = db.TextProperty(required=True)
