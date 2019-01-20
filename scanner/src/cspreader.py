#!/usr/bin/env python3
#
# Simple script showing how to read a mitmproxy dump file
#
from mitmproxy import io
from mitmproxy.exceptions import FlowReadException
import pprint
import sys
import json

with open(sys.argv[1], "rb") as logfile:
    freader = io.FlowReader(logfile)
    pp = pprint.PrettyPrinter(indent=4)
    try:
        for f in freader.stream():
            if f.request.path == "/cspscannerreport":
                # print ("=========== Report Found =============")
                # print (f.request.content)
                print ("  =========== ")
                print ("Blocked URI: " + json.loads(f.request.content)['csp-report']['blocked-uri'])
                # print ("original-policy: " + json.loads(f.request.content)['csp-report']['original-policy'])
                print ("violated-directive: " + json.loads(f.request.content)['csp-report']['violated-directive'])
                print ("document-uri: " + json.loads(f.request.content)['csp-report']['document-uri'])
                if 'line-number' in json.loads(f.request.content)['csp-report']:
                    print ("line-number: " + str(json.loads(f.request.content)['csp-report']['line-number']))
                if 'source-file' in json.loads(f.request.content)['csp-report']:
                    print ("source-file: " + json.loads(f.request.content)['csp-report']['source-file'])
                # print (json.loads(f.request.content)['csp-report'].keys())
                # sys.exit()                
            else:
                print (".... not a report ....")
            # print(f)
            # print(f.request.host)
            # pp.pprint(f.get_state())
            # print("")
    except FlowReadException as e:
        print("Flow file corrupted: {}".format(e))
