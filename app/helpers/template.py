from google.appengine.ext.webapp import template


def render(template_source, template_values):
    path = 'templates/' + template_source + '.html'
    return template.render(path, template_values)
