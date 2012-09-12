from datetime import datetime, timedelta


# ISO8601 date string to datetime parser
def parse_iso8601_datetime(dtstr, loose=False):
    """
    Convert ISO8601 datetime string and return Python datetime.datetime.
    Specify loose=True for more relaxed parsing accepting eg "YYYY-MM-DD" format.

    Raise ValueError on malformed input.
    reference: http://stackoverflow.com/questions/8569396/storing-rss-pubdate-in-app-engine-datastore#answer-8570029
    """
    dt = None
    if len(dtstr) == 19:    # (eg '2010-05-07T23:12:51')
        dt = datetime.strptime(dtstr, "%Y-%m-%dT%H:%M:%S")
    elif len(dtstr) == 20:  # (eg '2010-05-07T23:12:51Z')
        dt = datetime.strptime(dtstr, "%Y-%m-%dT%H:%M:%SZ")
    elif len(dtstr) == 25:  # (eg '2010-05-07T23:12:51-08:00')
        dt = datetime.strptime(dtstr[0:19], "%Y-%m-%dT%H:%M:%S")
        tzofs = int(dtstr[19:22])
        dt = dt - timedelta(hours=tzofs)
    else:
        if loose:
            if len(dtstr) == 10:  # (eg '2010-05-07')
                dt = datetime.strptime(dtstr, "%Y-%m-%d")
        if not dt:
            raise ValueError("Invalid ISO8601 format: '%s'" % dtstr)
    return dt
