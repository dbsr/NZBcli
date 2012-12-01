#!/usr/bin/env python
# encoding: utf-8
# daanmathot@gmail.com
# Sat Dec  1 08:31:51 2012

"""
nzbcli.exceptions
~~~~~~~~~~~~~~~~~

Custom exceptions for NZBCli

"""


class NZBCliException(Exception):
    pass


class ConfigError(NZBCliException):
    pass


class NZBCliError(NZBCliException):
    pass
