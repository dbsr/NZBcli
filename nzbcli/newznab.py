#!/usr/bin/env python
# encoding: utf-8
# daanmathot@gmail.com
# Sat Dec  1 08:23:44 2012


"""
nzbcli.newznab
~~~~~~~~~~~~~~

This module is used an interface between NZBCli and newznab.
The do_query returns a list of dictionaries with relevant data. The category
argument is optional.

"""


import urllib
import json

import nzbcli
from nzbcli import utils
from nzbcli.exceptions import NZBCliError


def do_query(query, category=None, DEBUG=False):
   # Create the payload
    param = {
        'q': query,
        't': 'search',
        'apikey': nzbcli.NEWZNAB_KEY,
        'maxage': nzbcli.RETENTION,
        'limit': 100,
        'attrs': 'size,group,poster,grabs',
        'o': 'json'
    }

    if category:
        param.update({'cat': nzbcli.CATEGORIES[category]})

     # Create the URL
    url = '{newznab_url}/api?{params}'.format(newznab_url=nzbcli.NEWZNAB_URL,
                                              params=urllib.urlencode(param))

    # make the request and convert the json object to a dictionary
    if DEBUG:
        import pickle
        f = open('pickle2', 'r')
        json_dict = pickle.load(f)
        f.close()
        return json_dict
    else:
        json_req = urllib.urlopen(url)
        json_dict = json.loads(json_req.read())

        num_results = int((json_dict.get('channel').get('response').get('@attributes')
                            .get('total', 0)))

        if num_results == 0:
            raise NZBCliError("The query '%s' returned no results" % query)
        elif num_results == 1:
            return [parse_item(json_dict['channel']['item'])]
        else:
            return [parse_item(x) for x in json_dict['channel']['item']]


def parse_item(item):
    return {
        'title': item['title'],
        'age': utils.date_to_days(item['pubDate']),
        '_pubdate': item['pubDate'],
        '_size': item['attr'][2]['@attributes']['value'],
        'size': utils.pretty_size(
            item['attr'][2]['@attributes']['value']),
        'grabs': item['attr'][5]['@attributes']['value'],
        '_poster': item['attr'][4]['@attributes']['value'],
        '_group': item['attr'][6]['@attributes']['value']
    }
