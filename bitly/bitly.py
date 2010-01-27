#!/usr/bin/python

import os
import sys
import urllib
import simplejson as json

API_URL = 'http://api.bit.ly'
API_VERSION = '2.0.1'

class APIError (Exception):
    '''Raised by BitLy instances in the event of errors returned by the 
    bit.ly REST API.  An APIError instance provides the following
    attributes:

    - *code* -- The numeric error code returned by bit.ly.
    - *message* -- The textual error message returned by bit.ly.
    - *result* -- The BitLy object associated with this exception
      (may be None).
    '''

    def __init__ (self, code, message, result=None):
        super(APIError, self).__init__()
        self.errorCode = code
        self.errorMessage = message
        self.result = result

    def __str__ (self):
        return 'Bit.ly API error: %d: %s' % (self.errorCode,
                self.errorMessage)

class BitLy (object):
    '''BitLy is a wrapper over the bit.ly REST API 
    (http://code.google.com/p/bitly-api/wiki/ApiDocumentation).  API
    calls are generated dynamically by the ``__getattr__`` method, and
    arbitrary keyword arguments are converted into URL parameters.

    Example usage::

    >>> api = bitly.BitLy(api_user, api_key)
    >>> res = api.shorten(longUrl='http://github.com/larsks')
    >>> print res['http://github.com/larsks']['shortUrl']
    http://bit.ly/9KKBJH

    '''

    api_version = API_VERSION
    api_url     = API_URL

    def __init__ (self, api_user, api_key):
        self.api_user = api_user
        self.api_key = api_key

        # Check credentials: this calls the errors() method, which
        # will raise an exception if we have invalid credentials
        # (or a bad URL, etc).
        res = self.errors()

    def _build_query_string(self, kwargs):
        params = {
                'version'   : self.api_version,
                'login'     : self.api_user,
                'apiKey'    : self.api_key,
                }

        params.update(kwargs)
        return urllib.urlencode(params)

    def __getattr__ (self, func):
        '''Generates a function that calls *func* via the bit.ly
        REST api.  Transforms any keyword arguments into URL 
        paramters.

        Returns a Python dictionary containing the result of the bit.ly 
        method call.

        Raise bitly.APIError on errors returned by bit.ly.'''

        def _ (**kwargs):
            url = '/'.join([self.api_url, func])
            query_string = self._build_query_string(kwargs)
            fd = urllib.urlopen(url, query_string)
            res = json.loads(fd.read())

            if res['errorCode'] != 0:
                raise APIError(
                        res['errorCode'],
                        res['errorMessage'],
                        res)
            elif not 'results' in res:
                raise APIError(-1, 'Unexpected response from bit.ly.', res)

            return res['results']

        return _

def main():
    '''Reads configuration from the [bitly] section of
    ~/.bitly.  Returns a BitLy() object to the caller.  This is 
    primarily during development -- if you load this module
    from the command line with ``python -i bitly/bitly.py``, the
    ``api`` object will be available to you for testing.'''

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

