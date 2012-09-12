formats_list = ['text/html', 'text/plain', 'application/json']
short_formats = ['html', 'plain', 'json']


def get(formatGet, acceptHeader):
    formats = formats_list
    format = ''
    if formatGet == '':  # If format is not set in the querystring, find the format from accept headers
        acceptHeader = acceptHeader.partition(',')[0]
        if acceptHeader in formats:  # If request headers are valid, give them the highest prio answer
            format = acceptHeader
        else:  # If acceptHeader doesn't contain a supported format, use text/plain
            format = formats[1]
    else:  # if format is set in querystring, then use the specified one.
        if not formatGet in formats:
            if not formatGet in short_formats:  # if format string is not valid, fallback to text/plain
                format = formats[1]
            else:
                format = formats[short_formats.index(formatGet)]
    return format


def formats():
    return formats_list
