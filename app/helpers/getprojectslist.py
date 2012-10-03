from google.appengine.api import memcache

from app.helpers.getversiondetailed import getProjectMeta
from app.models import Project


def getProjectsList():
    p = memcache.get('projectsList')
    if not p:
        ps = Project.all()
        p = []
        for project in ps:
            p.append(project.project)
        p.sort()
        memcache.set('projectsList', p, 600)

    return p


def getProjectsListDetailed():
    ps = getProjectsList()
    projects = []
    for project in ps:
        data = getProjectMeta(project)
        if data['prettyname']:
            prettyname = data['prettyname']
        else:
            prettyname = project

        projects.append((prettyname, project))

    return projects
