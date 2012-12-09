#!/usr/bin/env python
# encoding: utf-8
# daanmathot@gmail.com
# Sat Dec  1 08:27:21 2012

"""
nzbcli.nzbindex
~~~~~~~~~~~~~~~

This module is uses the nzbindex.nl rss feed to fetch nzb urls based on several
parameters.

@TODO:
    - better (any) error handling.
    - supplement poor newznab nzb results with an open nzbindex search

"""

import urllib

from BeautifulSoup import BeautifulSoup


def get_links(nzb_list):
    for nzb in nzb_list:
        # create the URL, format A (strict). Might add a less strict,
        # fail safe query later, for now satisfied with success percentage
        age = int(nzb['age'][:-1])
        params = {
            'poster': nzb['_poster'],
            'minage': max(age - 1, 0),
            'maxage': age + 1,
            'minsize': max(int((float(nzb['_size']) / float(1024 * 1024)) - 25), 0),
            'maxsize': int((float(nzb['_size']) / float(1024 * 1024)) + 25),
            'q': nzb['title']
        }
        url = "http://nzbindex.nl/rss/{groupname}/?{params}".format(
            groupname=nzb['_group'], params=urllib.urlencode(params))

        req = urllib.urlopen(url)

        soup = BeautifulSoup(req.read())

        try:

            nzb_url = soup.find(name='enclosure').get('url', None)

        except AttributeError:

            nzb_url = None

        yield {
            'url': nzb_url,
            'title': nzb['title']
        }
