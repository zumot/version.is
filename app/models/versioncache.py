from google.appengine.ext import db


# Version database model
class VersionCache(db.Model):
    project = db.StringProperty(required=True)
    version = db.StringProperty(required=True)
    commit = db.StringProperty(required=True)
    date = db.DateTimeProperty(required=True)
