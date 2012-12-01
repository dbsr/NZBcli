#!/usr/bin/env python
# encoding: utf-8
# daanmathot@gmail.com
# Sat Dec  1 08:28:38 2012

"""
nzbcli.__init__
~~~~~~~~~~~~~~~

Used for variable storage and the config parser.

"""


import ConfigParser
import os

from nzbcli.exceptions import NZBCliError

RETENTION = None
SABNZBD_HOST = None
SABNZBD_KEY = None
SABNZBD_BASEURL = None
NEWZNAB_KEY = None
NEWZNAB_URL = None


def read_config():

    global RETENTION, SABNZBD_KEY, NEWZNAB_URL, NEWZNAB_KEY, \
            SABNZBD_BASEURL, SABNZBD_CATEGORY

    cfg = ConfigParser.RawConfigParser(allow_no_value=False)

    try:
        cfg.readfp(open(os.path.join(os.getenv('HOME'), '.nzbcli.cfg'), 'r'))

    except IOError:
        raise NZBCliError("Could not read from:  ~/.nzbcli.cfg")

    RETENTION = cfg.get('general', 'retention')
    # Build the sabnzbd base url
    SABNZBD_BASEURL = "http://{host}:{port}/sabnzbd/".format(
        host=cfg.get('sabnzbd', 'host'), port=cfg.get('sabnzbd', 'port'))
    SABNZBD_CATEGORY = cfg.get('sabnzbd', 'use_category')
    SABNZBD_KEY = cfg.get('sabnzbd', 'nzb_key')
    NEWZNAB_URL = cfg.get('newznab', 'url')
    NEWZNAB_KEY = cfg.get('newznab', 'api_key')

# Static constants

VERSION = '0.1'
CATEGORIES = {
    'HDTV': '5040',
    'SDTV': '5030',
    'HDMOVIE': '2040',
    'SDMOVIE': '2030',
    'AUDIOBOOK': '3030',
    'MP3': '3010',
    'LOSSLESS': '3040',
    'ALL': 0
}
