#!/usr/bin/env python
# encoding: utf-8
# daanmathot@gmail.com
# Sun Dec  9 06:18:34 2012


"""
nzbcli.newznab
~~~~~~~~~~~~~~

This module is used an interface between NZBCli and newznab.
The do_query returns a list of dictionaries with relevant data. The category
argument is optional.

"""


import urllib
import requests
import re

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
        'attrs': 'size,group,poster,grabs,category',
        'o': 'json'
    }

    if category:
        param.update({'cat': nzbcli.CATEGORIES[category]})

     # Create the URL
    url = '{newznab_url}/api?{params}'.format(newznab_url=nzbcli.NEWZNAB_URL,
                                              params=urllib.urlencode(param))

    # make the request and convert the json object to a dictionary
    json_req = requests.get(url)
    json_dict = json_req.json

    num_results = int((json_dict.get('channel').get('response').get('@attributes')
                            .get('total', 0)))

    if num_results == 0:
        raise NZBCliError("The query '%s' returned no results" % query)
    elif num_results == 1:
        results = [parse_item(json_dict['channel']['item'])]
    else:
        results = [parse_item(x) for x in json_dict['channel']['item']]

    if nzbcli.FILTER:
        results = filter_foreign(results)
        if not len(results) > 0:
            raise NZBCliError("No results after applying filter.")

    return results


def filter_foreign(results):
    rgx = re.compile(r'.*\b(german|ita|french|de|deutch|das)\b.*',
                     re.IGNORECASE)
    _results = []
    for result in results:
        if not re.match(rgx, result['title']):
            _results.append(result)

    return _results


def parse_item(item):
    # max lenght for table
    if len(item['title']) > 80:
        item['title'] = item['title'][:78] + '..'
    return {
        'title': item['title'].encode('utf-8').strip(),
        'age': utils.date_to_days(item['pubDate']),
        'category': item['category'],
        '_pubdate': item['pubDate'],
        '_size': item['attr'][2]['@attributes']['value'],
        'size': utils.pretty_size(
            item['attr'][2]['@attributes']['value']),
        'grabs': item['attr'][5]['@attributes']['value'],
        '_poster': item['attr'][4]['@attributes']['value'],
        '_group': item['attr'][6]['@attributes']['value']
    }
