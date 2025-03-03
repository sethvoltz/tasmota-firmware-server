#!/usr/bin/env python3
# coding=utf-8
"""
server.py - firmware server for Tasmota OTA upgrade

Copyright (C) 2019 Gennaro Tortone
Copyright (C) 2024 Seth Voltz

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

Instructions:
  See README.md
"""

import os.path
from optparse import OptionParser
from sys import exit

from flask import Flask, send_file
import netifaces as ni

usage = "usage: server {-d | -i} arg"

parser = OptionParser(usage)
parser.add_option("-d", "--dev", action="store", type="string",
                  dest="netdev", default="en0", help="network interface (default: en0)")
parser.add_option("-i", "--ip", action="store", type="string",
                  dest="ip", help="IP address to bind")
parser.add_option("-f", "--fwdir", action="store", type="string",
                  dest="fwdir", help="firmware absolute path directory (default: firmware/ directory)")
(options, args) = parser.parse_args()

netip = None

if options.ip is None:
    try:
        netip = ni.ifaddresses(options.netdev)[ni.AF_INET][0]['addr']
    except Exception as e:
        print("E: network interface error - {}".format(e))
        exit(1)
else:
    netip = options.ip

if options.fwdir is None:
    fwdir = os.path.dirname(os.path.realpath(__file__)) + "/firmware/"
else:
    if os.path.isdir(options.fwdir):
        fwdir = options.fwdir
    else:
        print("E: directory " + options.fwdir + " not available")
        exit(1)

print(" * Directory: " + fwdir)

app = Flask(__name__)


@app.route('/<filename>')
def fw(filename):
    if os.path.exists(fwdir + str(filename)):
        return send_file(fwdir + str(filename),
                         download_name=filename,
                         mimetype='application/octet-stream')

    return "ERROR: file not found"


if __name__ == "__main__":
    try:
        app.run(host=netip, port=38266)
    except Exception as e:
        print("E: {}".format(e))
