from google.appengine.ext import db


# Version database model
class ShaCache(db.Model):
    project = db.StringProperty(required=True)
    sha = db.StringProperty(required=True)
