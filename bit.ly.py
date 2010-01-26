#!/usr/bin/python

import os
import sys
import urllib
import optparse
from ConfigParser import ConfigParser
import simplejson as json

API_URL = 'http://api.bit.ly'
API_VERSION = '2.0.1'

class BitLy (object):
    api_version = API_VERSION

    def __init__ (self, api_user, api_key):
        self.api_user = api_user
        self.api_key = api_key

    def __getattr__ (self, f):
        def _ (**kwargs):
            d = {
                    'version'   : self.api_version,
                    'login'     : self.api_user,
                    'apiKey'    : self.api_key,
                    }

            d.update(kwargs)

            url = '/'.join([API_URL, f])
            query = urllib.urlencode(d)

            fd = urllib.urlopen(url, query)
            return json.loads(fd.read())

        return _

def parse_args():
    p = optparse.OptionParser()
    p.add_option('-f', '--config', default='~/.bitly')
    return p.parse_args()

def main():
    opts, args = parse_args()

    config = ConfigParser()
    config.read(os.path.expanduser(opts.config))

    if not config.has_section('bitly'):
        print >>sys.stderr, 'Failed to read bit.ly API configuration ' \
                'from %s.' % opts.config
        sys.exit(1)

    bitly = BitLy(
            config.get('bitly', 'api_user'),
            config.get('bitly', 'api_key'),
            )

    if args:
        url = args[0]
    else:
        url = sys.stdin.readline().strip()

    res = bitly.shorten(longUrl=url)

    if 'results' in res and url in res['results'] \
            and 'shortUrl' in res['results'][url]:
        print res['results'][url]['shortUrl']
    else:
        print >>sys.stderr, 'ERROR: Failed to generate short URL.'
        print url

if __name__ == '__main__':
    main()

