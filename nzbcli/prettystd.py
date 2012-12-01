#!/usr/bin/env python
# encoding: utf-8
# daanmathot@gmail.com
# Sat Dec  1 08:30:09 2012

"""
nzbcli.prettystd
~~~~~~~~~~~~~~~~

This module handles data/ui presentation.

@TODO:
    - Better stderr handling (uses stdout for now, which is, so Ive heard, a
      terrible sin).

"""


from termcolor import colored
from printio import PrettyValues

TITLE = 'blue'
SUBTITLE = 'cyan'
KEYWORD = 'green'
ERROR = 'red'


def out(msg, format_dict=None, indent=0, newline=True):
    if format_dict:
        for key, value in format_dict.iteritems():
            format_dict.update({key: colored(value, KEYWORD)})
        _msg(msg.format(**format_dict), indent, newline)
    else:
        _msg(msg, indent, newline)


def err(msg, format_dict, indent, newline=True):
    for key, value in format_dict.iteritems():
        format_dict.update({key: colored(value, ERROR)})

    _msg(msg.format(**format_dict), indent, newline)


def _msg(msg, indent, newline):
    if newline:
        print

    print "{0} {1}".format(" " * indent, msg)


def table(results, print_num=True):
    pv = PrettyValues()

    if print_num:
        for i, r in enumerate(results):
            r.update({'num': i})
        pv.newcol('num')

    pv.newcol('title')
    pv.newcol('size')
    pv.newcol('age')
    pv.newcol('grabs')
    print pv.text(results)
