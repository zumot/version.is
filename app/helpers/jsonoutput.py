import json


def jsonOutput(content, callback):
    if callback != '':
        content = json.dumps(content, separators=(',', ':'))
        content = callback + '(' + content + ');'
    else:
        content = json.dumps(content, indent=2)

    return content
