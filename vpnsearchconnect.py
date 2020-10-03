# -*- coding: utf-8 -*-

import csv
import urllib
import json
import os.path
import sys
import base64
import subprocess
from subprocess import Popen

# script path
scriptpath = os.path.abspath(os.path.dirname(__file__)) + "/"

# args
args = sys.argv

# read cache
data = {}
if os.path.exists(scriptpath + "vsc.txt"):
    f = open(scriptpath + "vsc.txt", "r")
    data = json.load(f)
    f.close()

# read region
f = open(scriptpath + "region.txt", "r")
region = json.load(f)
f.close()

# read VPN list
res1 = urllib.urlopen("https://www.vpngate.net/api/iphone/")
cr = csv.reader(res1)

# search vpn server
print "\n--------------------------------------------------------"
print "Searching VPN server in the following region."
print "--------------------------------------------------------"
for i,r in enumerate(args):
    if i != 0:
        print region[int(r)-1]
print "--------------------------------------------------------"

for row in cr:
    if len(row) == 15 and row[6] == "JP":
        region_code = 0
        if data.has_key(row[1]):
            region_code = data[row[1]]
        else:
            # get region_code
            print "Searching the region of IP(" + row[1] + ")."
            res2 = urllib.urlopen("https://freegeoip.app/json/" + row[1])
            iptoaddrs = json.load(res2)
            if iptoaddrs["region_code"] != "":
                region_code = int(iptoaddrs["region_code"])
                data[row[1]] = region_code
                f = open(scriptpath + "vsc.txt", "w")
                json.dump(data, f)
                f.close()
            else:
                print "Cannot identify the region of IP(" + row[1] + ")."
        if region_code != 0:
            print "Region of " + row[0] + " (" + row[1] + ") => " + str(region_code) + ":" + region[region_code-1]
            # search region
            for i,arg in enumerate(args):
                if i != 0 and int(arg) == region_code:
                    print "Connecting to " + row[0] + "... Please wait."
                    # Base64 decode
                    ovpn = base64.b64decode(row[14])
                    # make .ovpn
                    f = open(scriptpath + "vpnovpn.ovpn", "w")
                    f.write(ovpn)
                    f.close()
                    # vpn connect
                    com = "/usr/sbin/openvpn " + scriptpath + "vpnovpn.ovpn"
                    proc = Popen(com, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    while True:
                        line = proc.stdout.readline()
                        if line.find("failed") > -1:
                            print "Connection failed: " + row[0]
                            break
                        elif line.find("Initialization Sequence Completed") > -1:
                            print "--------------------------------------------------------"
                            print "Connection success: "
                            print "\t" + row[0] + " (" + row[1] + ") => " + str(region_code) + ":" + region[region_code-1]
                            print "--------------------------------------------------------"
                            sys.exit(0)
print "--------------------------------------------------------"
print "Cannot find a valid VPN server."
print "--------------------------------------------------------"
sys.exit(-1)
