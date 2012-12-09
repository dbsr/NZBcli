#!/usr/bin/env python
# encoding: utf-8
# daanmathot@gmail.com
# Mon Nov 26 04:43:09 2012

import argparse
import re
import urllib
import os

import nzbcli
from nzbcli.exceptions import NZBCliError
from nzbcli import prettystd, newznab, nzbindex


def main(query, param_dict):
    # Make sure we got a clean config file
    try:
        nzbcli.read_config(args)
    except NZBCliError, e:
        prettystd.err(
            msg="{cfgError}! {e}\n".format(cfgError='{cfgError}', e=e),
            format_dict={'cfgError': 'NZBCliError'},
            indent=0,
            newline=True
        )
        return 1

    # Simple header
    prettystd.out(
        msg='{title} {version}0.1: A commandline nzb browser/downloader.',
        format_dict={'title': 'NZBCli', 'version': 'v'},
        indent=0,
    )
    # Initiating search
    prettystd.out(
        msg="{indent} Starting NZB search for '{query}' (category: {category}).",
        format_dict={'indent': '>', 'query': query, 'category': args['category']},
        indent=0)
    # Query the newznab provider
    try:
        results = newznab.do_query(query=query, category=args['category'])
    except NZBCliError:
        prettystd.err(
            msg="-> {title}... :(",
            format_dict={'title': 'no results'},
            indent=1,
        )
        return 1
    # Present results and get download targets
    print results
    download_list = _present_results(results)

    if download_list is None:
        return

    # Retrieve nzburls using the rss api from nzbindex.nl
    for url in nzbindex.get_links(download_list):
        # Print success/fail
        if url['url']:
            success = 'OK!'
            # Send nzb url to sabnzbd
            params = {
                'apikey': nzbcli.SABNZBD_KEY,
                'mode': 'addurl',
                'name': url['url']
            }
            # Send category param?
            if nzbcli.SABNZBD_CATEGORY and args['category']:
                params.update({'category': args['category']})

            sab_url = nzbcli.SABNZBD_BASEURL + 'api?' + urllib.urlencode(params)
            urllib.urlopen(sab_url)

        else:
            success = 'FAIL'

        # TODO: add a real sabnzbd success check, inline (using blessings?)
        # buffer updates

        prettystd.out(
            msg="> {title} ==> {success} ==> {sab} ==> {ok}",
            format_dict={'title': url['title'],
                         'success': success,
                         'sab': 'sabnzbd',
                         'ok': success},
            indent=6,
            newline=False
        )

    goodbye()


def _present_results(results):
    prettystd.out(
        msg='{indent} {num} results:\n',
        format_dict={'indent': '>>', 'num': len(results)},
        indent=0,
        newline=True
    )
    prettystd.table(results)
    # Get user picks
    valid_choice = None
    try:
        while not valid_choice:
            raw_choice = raw_input('\n >>> Download: num (eg. 2 or 1,3-5) / (A)ll / (N)one: ')
            valid_choice = _validate_choice(raw_choice, len(results))
        # Exit NZBCli
        if valid_choice == 'N':
            return
    except KeyboardInterrupt:
        # Cleanly exit nzbcli:
        goodbye()
        return

    # Confirm user picks:
    prettystd.out(
        msg='{indent} retrieving links for the following {nzb}(s): {nzb_nums}\n',
        format_dict={'indent': '>>>>', 'nzb': 'nzb',
            'nzb_nums': str(valid_choice).strip('[]')},
        indent=0,
        newline=True
    )

    return [results[x] for x in valid_choice]


def _validate_choice(raw_choice, len_results):
    # Make sure choices are valid
    if raw_choice == 'A' or raw_choice == 'a':
        return range(0, len_results)
    elif raw_choice == 'N' or raw_choice == 'n':
        return 'N'
    elif re.match(r'^[0-9,-]+$', raw_choice):
        # split str into single digits and ranges. Note: I bet someone
        # smart would use an iterator here. 8)
        digits = []

        for digit in raw_choice.split(','):
                # make sure its a digit, its in the result range and
                # unique. Also, should we correct possible typos or raise
                # an Exception as soon as we find an invalid digit range?
            if (re.match(r'^[0-9]+$', digit) and
                int(digit) in range(0, len_results + 1) and
                    int(digit) not in digits):
                        digits.append(int(digit))
            elif re.match(r'[0-9]+-[0-9]+', digit):
                d_range = digit.split('-')
                if re.match(r'[0-9]+', (d_range[0] + d_range[1])):
                    if int(d_range[0]) < int(d_range[1]):
                        for d in range(int(d_range[0]), int(d_range[1]) + 1):
                            if (int(d) not in digits and
                                    int(d) in range(0, len_results + 1)):
                                digits.append(int(d))

        if len(digits) != 0:
            return digits

    # Only invalid entries should end up here
    prettystd.err(
        msg='{error}: Invalid choice, please {try} again.',
        format_dict={'error': 'Error', 'try': 'try'},
        indent=1,
        newline=True
    )
    return None


def goodbye():
    prettystd.out(
        msg='\n{title} / Nov 31, 2012 / {version}0.1 / dbsr{at}moscownights.nl' \
            ' {indent} Thanks for chosing bla, we hope, etc...!\n',
            format_dict={'title': 'NZBCli', 'version': 'v', 'at': '@',
                            'indent': '>>>'},
        indent=0,
        newline=True
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Search and download nzb's from the commandline.",
        epilog="Edit the config file 'nzbcli.cfg.example' and copy it to"\
        " your home directory; '~/.nzbcli.cfg', before running NZBCli.py")
    parser.add_argument('query',
                        type=str,
                        help="the search query, eg: 'Arrested Development S01E01'")
    parser.add_argument('--category', '-c',
                        type=str,
                        dest='category',
                        required=False,
                        default=None,
                        help="eg. 'HDTV' (or 'HDMOVIE', 'SDTV', 'SDMOVIE', \
                                'MP3', 'AUDIOBOOK', 'PRON', etc)."),
    parser.add_argument('--filter-foreign', '-f',
                        type=bool,
                        dest='filter',
                        required=False,
                        default=None,
                        help="filter non english results (can also be set as \
                        default in the config file)."),
    parser.add_argument('--config', '-C',
                        type=str,
                        dest='custom_config_location',
                        required=False,
                        default=None,
                        help="eg. '/path/to/nzbcli.cfg'")
    args = vars(parser.parse_args())
    query = args['query']

    sane_parameters = True
    # validate category parameter
    if args['category']:
        try:
            assert args['category'] in nzbcli.CATEGORIES
        except AssertionError:
            prettystd.err(
                msg="NZBCli: '{e_category}' is not a valid category.",
                format_dict={'e_category': args['category']},
                indent=0,
                newline=False
            )
            sane_parameters = False
    # validate custom_config_location parameter
    if args['custom_config_location']:
        custom_config_location = args['custom_config_location']
        try:
            assert os.path.isfile(custom_config_location)
        except AssertionError:
            prettystd.err(
                msg="NZBCli: '{cfg_file}' is not a valid config file.",
                format_dict={'cfg_file': custom_config_location},
                indent=0,
                newline=False
            )
            sane_parameters = False

    if sane_parameters:
        # valid args, continue:
        main(query, args)
