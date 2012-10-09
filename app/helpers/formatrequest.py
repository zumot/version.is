""" Attempts to get format from the request

jquery.json -> ('jquery', 'application/json')
jquery.txt  -> ('jquery', 'text/plain')
jquery      -> ('jquery', None)

"""

def getFormatFromRequest(input):
    if input[-4:] == '.txt':
        return (input[:-4], 'text/plain')
    elif input[-5:] == '.json':
        return (input[:-5], 'application/json')
    else:
        return (input, None)

