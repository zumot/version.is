from google.appengine.ext import db


# Version database model
class Project(db.Model):
    project = db.StringProperty(required=True)
    data = db.StringProperty(required=True)
