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

License
=======

Copyright (C) 2010 Lars Kellogg-Stedman

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

.. _bit.ly api: http://code.google.com/p/bitly-api/wiki/ApiDocumentation

