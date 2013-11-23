#!/usr/bin/env python

import sys, zope.interface
from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen

class DasOertlicheDeResolver:

    def findName(self, number):
        data = urlopen("http://www.dasoertliche.de/Controller?form_name=search_inv&js=no&ph=%s" % number)
        soup = BeautifulSoup(data.read().decode("iso-8859-15"))

        entry_0 = soup.find(attrs={'id': 'entry_0'})
        if entry_0 is not None:
            return entry_0.findNext("a").findNext("span").text.replace("&nbsp;", "").encode("utf-8")
        return "Unknown"

def main():
    kt = DasOertlicheDeResolver()
    print("Is %s implementing the ReverseSearchInterface?" % kt.__class__.__name__)

    print("... %s" % INumberResolver.providedBy(kt))
    print("")
    print(kt.findName("042643113"))
    print(kt.findName("042641331"))
    print(kt.findName("042643161"))
    print(kt.findName("04288 392"))


if __name__ == '__main__':
    main()

