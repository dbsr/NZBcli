NZBcli v0.1
===========
Search and download nzb's from the commandline.


DESCRIPTION:

    NZBcli is a small, basic commandline tool to search and download newsgroup releases. It relies heavily on the api from the newsgroup indexer newznab. It should
    work fine on similar sites making use of a similar API (some adjustments might be necesarry).


SABNZBD INTEGRATION:

    NZBcli also has very basic sabnzbd integration. The user can chose nzb's from the results and send them directly to sabnzbd.


CONFIGURATION:

    Before NZBCli can work it needs some initial configuration settings. The
    default location for the config file is '~/.nzbcli.cfg'. This can be changed
    by using the '-C' parameter.


USAGE EXAMPLE:

    $ NZBcli 'Life and Times of Tim s01e01' -c 'HDTV'


BUGS:

    There will be lots of bugs. Please report them. TIA


~ Sat Dec  1 09:55:07 2012
