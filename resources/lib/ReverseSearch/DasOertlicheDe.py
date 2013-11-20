#!/usr/bin/python


import sys
import re
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen


class DasOertlicheDe:

    def __init__(self):
        pass


    def lookupName(self, callerid):
        data = urlopen("http://www.dasoertliche.de/Controller?form_name=search_inv&js=no&ph=%s" % callerid)
        lookup = data.read().decode('iso-8859-15')
        print(lookup)
        exp = re.compile('na: "([a-zA-Z0-9_ ]+)",', re.MULTILINE)
        lookup = exp.search(lookup)
        if lookup != None:
            sys.stdout.write(lookup.group(1))
            sys.stdout.flush()



do = DasOertlicheDe()
print(do.lookupName("042641331"))