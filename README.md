PyKlicktel
==========

Python Klicktel Phonebook API Handler

### Usage:

#### Commandline:

    Usage:
        ./klicktel.py --key=<apikey> meta --what=<str> --where=<str> [--parents-only]
        ./klicktel.py --key=<apikey> whitepages --prename=<str> --name=<str> --where=<str> [--parents-only]
        ./klicktel.py --key=<apikey> yellowpages --trade=<str> --companyname=<str> --where=<str> [--parents-only]
        ./klicktel.py --key=<apikey> invers --number=<int> [--parents-only]
        ./klicktel.py --key=<apikey> geo --distance=<int_as_km> --what=<str> --where=<str> [--parents-only]

#### Code:

    import klicktel
    kh = klicktel.Klicktel("api-key")
    print kh.meta_search("Jon Doe", "City").dict()

### Requirements:

* docopt for commandline mode

### Support me:

[![Flattr this git repo](http://api.flattr.com/button/flattr-badge-large.png)](https://flattr.com/submit/auto?user_id=shellshark&url=https://github.com/wrow/PyKlicktel&title=PyKlicktel&tags=github&category=software)
