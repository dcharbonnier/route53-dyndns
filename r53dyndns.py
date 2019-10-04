#! /usr/bin/env python
"""Updates a Route53 hosted A alias record with the current ip of the system.
"""
import dns.resolver
import boto.route53
import logging
import os
from optparse import OptionParser
import re
from re import search
import socket
import sys
import urllib2
import contextlib

parser = OptionParser()
parser.add_option('-R', '--record', type='string', dest='record_to_update', help='The A record to update.')
parser.add_option('-v', '--verbose', dest='verbose', default=False, help='Enable Verbose Output.', action='store_true')
(options, args) = parser.parse_args()

if options.record_to_update is None:
    logging.error('Please specify an A record with the -R switch.')
    parser.print_help()
    sys.exit(-1)
if options.verbose:
    logging.basicConfig(
        level=logging.INFO,
    )

def ip_with_dns():
    dns = (
        ('resolver1.opendns.com', 'myip.opendns.com'),
        ('ns1.google.com', 'o-o.myaddr.l.google.com')
    )
    for (nameserver, domain) in dns:
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers=[socket.gethostbyname(nameserver)]
            rdata = resolver.query(domain, 'A')[0]
            ip = str(rdata)
            return ip
        except:
            continue

def ip_with_http():
    check_ips = ('http://ipecho.net/plain',
                 'http://v4.ident.me',
                 'http://ipinfo.io/ip')
    for url in check_ips:
        try:
            with contextlib.closing(urllib2.urlopen(url, timeout=3)) as req:
                ip = req.read().strip()
                try:
                    socket.inet_aton(ip)
                except:
                    continue
            return ip
        except (urllib2.HTTPError,
                urllib2.URLError,
                socket.timeout):
            continue

def get_ip():
    ip = ip_with_dns()
    if ip is None:
        ip = ip_with_http()
    if ip is None:
        raise Exception("Can't get the current ip")
    return ip


current_ip = get_ip()
record_to_update = options.record_to_update
zone_to_update = '.'.join(record_to_update.split('.')[-2:])
logging.info('Current IP address: %s', current_ip)

try:
    socket.inet_aton(current_ip)
    conn = boto.route53.connect_to_region(os.getenv('AWS_CONNECTION_REGION', 'us-east-1'))
    zone = conn.get_zone(zone_to_update)
    for record in zone.get_records():
        if search(r'<Record:' + record_to_update, str(record)):
            if current_ip in record.to_print():
                logging.info('Record IP matches, doing nothing.')
                sys.exit()
            logging.info('IP does not match, update needed.')
            zone.delete_a(record_to_update)
            zone.add_a(record_to_update, current_ip)
            sys.exit()
    logging.info('Record not found, add needed')
    zone.add_a(record_to_update, current_ip)
except socket.error as e:
     print repr(e)
