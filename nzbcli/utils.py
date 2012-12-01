#!/usr/bin/env python
# encoding: utf-8
# daanmathot@gmail.com
# Sat Dec  1 08:27:47 2012

"""
nzbcli.utils
~~~~~~~~~~~~

Small utility module used by the different nzbcli modules.

"""


def pretty_size(size):
    """
    converts size in bytes to human readable string format.
    source: http://www.dzone.com/snippets/filesize-nice-units
    """
    size = int(size)
    suffixes = [("B", 2 ** 10), ("K", 2 ** 20), ("M", 2 ** 30), ("G", 2 ** 40)]
    for suf, lim in suffixes:
        if size > lim:
            continue
        else:
            return round(size / float(lim / 2 ** 10), 2).__str__() + suf


def date_to_days(date_string):
    from datetime import datetime
    """
    converts date string: Sun, 31 Dec 2012 0:00:00 -0000 to age in
    days eg: 3d
    """
    a = datetime.strptime(date_string[:-6], '%a, %d %b %Y %H:%M:%S')
    age = datetime.today() - a

    return "%dd" % age.days
