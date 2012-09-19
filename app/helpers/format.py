import logging


formats_list = ['text/html', 'text/plain', 'application/json']
short_formats = ['html', 'plain', 'json']


def get(formatGet, acceptHeader):
    # If no format is specified in the URI, parse the accept header.
    if formatGet == '':
        format = parseAcceptHeader(acceptHeader)
    # If a format is specified in the URI, use it.
    else:
        if not formatGet in formats_list:
            if not formatGet in short_formats:
                # If no matching format is found, fall back to text/plain
                format = 'text/plain'
            else:
                format = formats_list[short_formats.index(formatGet)]
    return format


def formats():
    return formats_list


""" Parsing an Accept Header to find the appropiate response format...

This is not a perfect solution. In the perfect world we would extract
all the different formats that the browser asked for, and then serve
the format that had the highest priority of the response formats that
we support.

But accept headers are of quite different structures. The purpose of
parsing the accept header is to make content negotiation doable by other
 means than get variables set in the querystring.

Thus, all we need to do, is to check if the highest priority is
text/plain or application/json, if that is the case, then serve the
appropiate format. If the accept header is empty, we will fall back to
text/plain, and for any other requests, we will just serve text/html.

While it is not the perfect solution, as we do not really implement
proper content negotiation, it is the best fit for us, as we do not want
to waste time doing unnecessary calculations.

"""


def parseAcceptHeader(acceptHeader):
    logging.info('Accept Header: ' + acceptHeader)
    highestPrio = acceptHeader.partition(',')[0]
    if highestPrio in ['text/plain', 'application/json']:
        return highestPrio
    else:
        if acceptHeader in ['', '*/*']:
            # default accept header in curl is */*
            return 'text/plain'
        else:
            return 'text/html'
