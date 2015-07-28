#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
from collections import namedtuple
import GeoIP


OUTPUT_FMT = "{0} - {country_code}, {region}, {region_name}, {city}, " + \
             "{area_code}"

# borrowed from https://gist.github.com/nathangrigg/2363393
regex = r'(?P<owner>\S+) (?P<bucket>\S+) (?P<time>\[[^]]*\]) (?P<ip>\S+) ' + \
        r'(?P<requester>\S+) (?P<reqid>\S+) (?P<operation>\S+) ' + \
        r'(?P<key>\S+) (?P<request>"[^"]*") (?P<status>\S+) ' + \
        r'(?P<error>\S+) (?P<bytes>\S+) (?P<size>\S+) (?P<totaltime>\S+) ' + \
        r'(?P<turnaround>\S+) (?P<referer>"[^"]*") ' + \
        r'(?P<useragent>"+?[^"]*"+?) (?P<version>\S)'
pattern = re.compile(regex)

fields = ['owner', 'bucket', 'time', 'ip', 'requester', 'reqid', 'operation',
          'key', 'request', 'status', 'error', 'bytes', 'size', 'totaltime',
          'turnaround', 'referer', 'useragent', 'version']

Message = namedtuple('Message', fields)


def handle_file(f):
    """Loop over lines in f and return list of log meessage tuples
    """
    msgs = []
    for line in f:
        m = pattern.match(line)
        if not m:
            print line
            raise Exception
        else:
            msgs.append(Message(**m.groupdict()))
    return msgs


def f1(m):
    """Filter messages that correspond to HTTP GET
    """
    return m.operation.startswith('WEBSITE.GET')


def f2(m):
    """Filter message where the useragent doesn't look like a bot
    """
    keywords = ['bot', 'spider', 'feedly', 'slurp']
    return not any(t in m.useragent.lower() for t in keywords)


def f3(m):
    """Filter messages for non-errors
    """
    return int(m.status) == 200


def main(argv):
    # object for geolocating requests
    gi = GeoIP.open(
        "/usr/local/var/GeoIP/GeoIPCity.dat",
        GeoIP.GEOIP_MEMORY_CACHE
    )

    # filtered list of message tuples
    log = []

    # loop over local directory containing AWS S3 logs, parsing into message
    # tuples before filtering
    for i in os.listdir(argv[1]):
        filename = os.path.join(argv[1], i)
        with open(filename, 'r') as f:
            log += filter(f3, filter(f2, filter(f1, handle_file(f))))

    # find the set of unique request IP addresses and geolocate them
    unique_ips = set(l.ip for l in log)
    for ip in unique_ips:
        gir = gi.record_by_addr(ip)
        if gir is not None:
            print(OUTPUT_FMT.format(ip, **gir))


if __name__ == '__main__':
    main(sys.argv)
