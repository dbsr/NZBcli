NZBcli v0.1
===========
Search and download nzb's from the commandline.


DESCRIPTION

NZBcli is a small, basic commandline tool to search and download newsgroup releases. It relies heavily on the api from the newsgroup indexer newznab. It should
work fine on similar sites making use of a similar API (some adjustments might be necesarry).


SABNZBD INTEGRATION

NZBcli also has very basic sabnzbd integration. The user can chose nzb's from the results and send them directly to sabnzbd.


CONFIGURATION

NZBcli reads its initial settings from '~/.nzbcli.cfg'. The parameter '-C /path/to/cfg.file' can be used to specify another location.

USAGE EXAMPLE

    $ NZBcli 'Life and Times of Tim s01e01' -c 'HDTV'


BUGS

Lots, probably, report them please. Thanks.

