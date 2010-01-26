#!/usr/bin/python

import os
import sys
import urllib
import simplejson as json

API_URL = 'http://api.bit.ly'
API_VERSION = '2.0.1'

class APIError (Exception):
    def __init__ (self, code, message, result=None):
        super(APIError, self).__init__()
        self.errorCode = code
        self.errorMessage = message
        self.result = result

    def __str__ (self):
        return 'Bit.ly API error: %d: %s' % (self.errorCode,
                self.errorMessage)

class BitLy (object):
    api_version = API_VERSION

    def __init__ (self, api_user, api_key):
        self.api_user = api_user
        self.api_key = api_key

        # check credentials
        res = self.errors()
        if res['errorCode'] != 0:
            raise APIError(res['errorCode'], res['errorMessage'])

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
            res = json.loads(fd.read())

            if res['errorCode'] != 0:
                raise APIError(
                        res['errorCode'],
                        res['errorMessage'],
                        res)
            return res

        return _

def main():
    from ConfigParser import ConfigParser
    cf = ConfigParser()
    cf.read(os.path.expanduser('~/.bitly'))

    api = BitLy(
            cf.get('bitly', 'api_user'),
            cf.get('bitly', 'api_key')
            )

    return api

if __name__ == '__main__':
    api = main()

