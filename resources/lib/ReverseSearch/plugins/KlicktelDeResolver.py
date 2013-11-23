#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from urllib2 import urlopen

class KlicktelDeResolver():
    def findName(self, number):
        data = urlopen("http://www.klicktel.de/rueckwaertssuche/%s" % number)
        lookup = data.read().decode('utf-8')
        exp = re.compile(r">1\. (.*)</a></h4>")
        resultName = exp.search(lookup)
        if resultName != None:
            return resultName.group(1).encode("utf-8")
        else:
            return "Unknown"

def main():
    kt = KlicktelDeResolver()
    print("Is %s implementing the ReverseSearchInterface?" % kt.__class__.__name__)

    print("... %s" % ResolverInterface.providedBy(kt))
    print("")
    print(kt.findName("042643113"))
    print(kt.findName("042641331"))
    print(kt.findName("042643161"))
    print(kt.findName("04288 392"))

if __name__ == '__main__':
    main()