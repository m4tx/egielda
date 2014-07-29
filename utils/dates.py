from datetime import datetime


def datetime_html_format(date):
    return date.strftime("%Y-%m-%dT%H:%M")


def string_to_datetime(date):
    tz_index = date.index('+')
    date = date[:tz_index] + date[tz_index:].replace(':', '')
    return datetime.strptime(date, '%Y-%m-%d %H:%M:%S%z')