import arrow
import os
import mimetypes



def datetimeformat(date_str):
    dt = arrow.get(date_str)
    return dt.humanize()


def file_type(filename):
    dump, ext = url.split('.')
    try:
        return mimetypes.types_map[ext]
    except KeyError():
        return 'Unknown'