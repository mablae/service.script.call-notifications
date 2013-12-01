#!/usr/bin/env python
# encoding: utf-8

__author__ = 'Frank Epperlein'
__doc__ = """
PyKlicktel
API-Info: http://openapi.klicktel.de/docs?id=11

Usage:
    ./klicktel.py --key=<apikey> meta --what=<str> --where=<str> [--parents-only]
    ./klicktel.py --key=<apikey> whitepages --prename=<str> --name=<str> --where=<str> [--parents-only]
    ./klicktel.py --key=<apikey> yellowpages --trade=<str> --companyname=<str> --where=<str> [--parents-only]
    ./klicktel.py --key=<apikey> invers --number=<int> [--parents-only]
    ./klicktel.py --key=<apikey> geo --distance=<int_as_km> --what=<str> --where=<str> [--parents-only]
"""

import urllib
import json
import random
import string

class KlicktelRequestException(Exception):
    pass

class KlicktelPhonenumber(object):

    def __init__(self, data):

        self.displayphone=False
        self.description=False
        self.countrycode=False
        self.area=False
        self.number=False
        self.pricing=False
        self.main=False
        self.type=False
        self.phone=False

        if 'displayphone' in data: self.displayphone=data['displayphone']
        if 'description' in data: self.description=data['description']
        if 'countrycode' in data: self.countrycode=data['countrycode']
        if 'area' in data: self.area=data['area']
        if 'number' in data: self.number=data['number']
        if 'pricing' in data: self.pricing=data['pricing']
        if 'main' in data: self.main=data['main']
        if 'type' in data: self.type=data['type']
        if 'phone' in data: self.phone=data['phone']

    def dict(self):
        return dict(
            displayphone=self.displayphone,
            description=self.description,
            countrycode=self.countrycode,
            area=self.area,
            number=self.number,
            pricing=self.pricing,
            main=self.main,
            type=self.type,
            phone=self.phone
        )

class KlicktelLocation(object):

    def __init__(self, data):

        self.country=False
        self.county=False
        self.district=False
        self.state=False
        self.street=False
        self.streetnumber=False
        self.zipcode=False

        if 'city' in data: self.city = data['city']
        if 'country' in data: self.country = data['country']
        if 'county' in data: self.county = data['county']
        if 'district' in data: self.district = data['district']
        if 'state' in data: self.state = data['state']
        if 'street' in data: self.street = data['street']
        if 'streetnumber' in data: self.streetnumber = data['streetnumber']
        if 'zipcode' in data: self.zipcode = data['zipcode']

    def dict(self):
        return dict(
            country=self.country,
            county=self.county,
            district=self.district,
            state=self.state,
            street=self.street,
            streetnumber=self.streetnumber,
            zipcode=self.zipcode
        )

class KlicktelEntry(object):

    def __init__(self, data):

        self.displayname=False
        self.entrytype=False
        self.firstname=False
        self.id=False
        self.lastname=False
        self.salutation=False
        self.locations=False
        self.phonenumbers=False

        if 'displayname' in data: self.displayname= data['displayname']
        if 'entrytype' in data: self.entrytype= data['entrytype']
        if 'firstname' in data: self.firstname= data['firstname']
        if 'id' in data: self.id= data['id']
        if 'lastname' in data: self.lastname= data['lastname']
        if 'salutation' in data: self.salutation= data['salutation']

        if 'location' in data:
            self.location = KlicktelLocation(data['location'])

        if 'phonenumbers' in data:
            self.phonenumbers = list()
            for number in data['phonenumbers']:
                self.phonenumbers.append(KlicktelPhonenumber(number))

    def dict(self):
        return dict(
            displayname=self.displayname,
            entrytype=self.entrytype,
            firstname=self.firstname,
            id=self.id,
            lastname=self.lastname,
            salutation=self.salutation,
            location=self.location.dict(),
            phonenumbers=[x.dict() for x in self.phonenumbers]
        )

class KlicktelResult(object):

    def __analyze(self, data):
        for entry in data:
            if entry['type'] == 'locations':
                for location in entry['locations']:
                    self.locations.append(KlicktelLocation(location))
            if entry['type'] == 'entries':
                for contact in entry['entries']:
                    self.entries.append(KlicktelEntry(contact))

    def __init__(self, data):
        self.locations = list()
        self.entries = list()
        self.__analyze(data)

    def dict(self):
        return dict(
            locations=[x.dict() for x in self.locations],
            entries=[x.dict() for x in self.entries]
        )

class Klicktel(object):

    def __requestid_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))

    def __init__(self, apikey, track=True):
        self.__apikey = apikey
        self.__requestid = self.__requestid_generator()

        if track:
            urllib.urlopen(
                "%s?%s" % ( "http://statistics.klicktel.de/trackingpix.png",
                            urllib.urlencode(dict(partner='OpenAPI3', requestid=self.__requestid))))

    def __request(self, url, params):
        result = urllib.urlopen("%s?%s" % (url, urllib.urlencode(params)))
        if result:
            json_data = result.read()
            data = json.loads(json_data)
            if 'response' in data and 'results' in data['response']:
                return data['response']['results']
            else:
                raise KlicktelRequestException('request failed, missing response/results (%s)' % data)

        else:
            raise KlicktelRequestException('request failed, result=%s' % result)

    def meta_search(self, what, where, parents_only=False):
        result = self.__request(
            "http://openapi.klicktel.de/searchapi/meta",
            dict(
                key=self.__apikey,
                requestid=self.__requestid,
                what=what,
                where=where,
                parents_only=parents_only))
        return KlicktelResult(result)

    def whitepages_search(self, prename, name, where, parents_only=False):
        result = self.__request(
            "http://openapi.klicktel.de/searchapi/whitepages",
            dict(
                key=self.__apikey,
                requestid=self.__requestid,
                prename=prename,
                name=name,
                where=where,
                parents_only=parents_only))
        return KlicktelResult(result)

    def yellowpages_search(self, trade, companyname, where, parents_only=False):
        result = self.__request(
            "http://openapi.klicktel.de/searchapi/yellowpages",
            dict(
                key=self.__apikey,
                requestid=self.__requestid,
                trade=trade,
                companyname=companyname,
                where=where,
                parents_only=parents_only))
        return KlicktelResult(result)

    def invers_search(self, number, parents_only=False):
        result = self.__request(
            "http://openapi.klicktel.de/searchapi/invers",
            dict(
                key=self.__apikey,
                requestid=self.__requestid,
                number=number,
                parents_only=parents_only))
        return KlicktelResult(result)

    def geo_search(self, distance, what, where, parents_only=False):
        result = self.__request(
            "http://openapi.klicktel.de/searchapi/geo",
            dict(
                key=self.__apikey,
                requestid=self.__requestid,
                distance=distance,
                what=what,
                where=where,
                parents_only=parents_only))
        return KlicktelResult(result)

if __name__ == '__main__':
    import docopt
    from pprint import pprint

    arguments = docopt.docopt(__doc__)

    klicktel = Klicktel(arguments['--key'])

    if arguments['meta']:
        pprint(klicktel.meta_search(arguments['--what'], arguments['--where'], arguments['--parents-only']).dict())
    if arguments['whitepages']:
        pprint(klicktel.whitepages_search(arguments['--prename'], arguments['--name'], arguments['--where'], arguments['--parents-only']).dict())
    if arguments['yellowpages']:
        pprint(klicktel.yellowpages_search(arguments['--trade'], arguments['--companyname'], arguments['--where'], arguments['--parents-only']).dict())
    if arguments['invers']:
        pprint(klicktel.invers_search(arguments['--number'], arguments['--parents-only']).dict())
    elif arguments['geo']:
        pprint(klicktel.geo_search(arguments['--distance'], arguments['--what'], arguments['--where'], arguments['--parents-only']).dict())

