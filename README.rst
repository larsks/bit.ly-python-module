=====================
Python bit.ly wrapper
=====================

This is a thin Python wrapper for the `bit.ly api`.  Basic usage looks like
this::

  >>> import bitlyapi
  >>> b = bitlyapi.BitLy(api_user, api_key)
  >>> url = 'http://www.google.com/'
  >>> res = b.shorten(longUrl=url)
  >>> 
  >>> print res[url]['shortUrl']
  http://bit.ly/6Hwstb

The return from any method call is a dict containing the results of
decoding the JSON returned from bit.ly.  For example::

  >>> import pprint
  >>> pprint.pprint(res)
  {'http://www.google.com/': {'hash': '2V6CFi',
                              'shortCNAMEUrl': 'http://bit.ly/6Hwstb',
                              'shortKeywordUrl': '',
                              'shortUrl': 'http://bit.ly/6Hwstb',
                              'userHash': '6Hwstb'}}

You can supply arbitrary keywords to method calls and they will be passed
to the bit.ly REST API::

  >>> res = b.shorten(longUrl=url,keyword='mycustomkeyword')

.. _bit.ly api: http://code.google.com/p/bitly-api/wiki/ApiDocumentation

