#!/usr/bin/env python3
#
# Simple script showing how to read a mitmproxy dump file
#
from mitmproxy import io
from mitmproxy.exceptions import FlowReadException
from optparse import OptionParser

import pprint
import sys
import json

parser = OptionParser()
parser.add_option("--ic", "--inline-scripts", dest="inline_scripts", default=False,
                  action="store_true",
                  help="Report on 'inline' script violations")

parser.add_option("--it", "--inline-styles", dest="inline_styles", default=False,
                  action="store_true",
                  help="Report on 'inline' style violations")

parser.add_option("--eval", "--eval-statements", dest="eval_statements", default=False,
                  action="store_true",
                  help="Report on 'eval' violations")

parser.add_option("--data", "--data-violations", dest="data_violations", default=False,
                  action="store_true",
                  help="Report on 'data' violations")

parser.add_option("--else", "--everything-else", dest="everything_else", default=False,
                  action="store_true",
                  help="Report violations not covered by other flags")


# parser.add_option("--is", "--inline-only", dest="inline_only", default=False,
#                   action="store_true",
#                   help="Only report on 'inline' violations")

# parser.add_option("-q", "--quiet",
#                   action="store_false", dest="verbose", default=True,
#                   help="don't print status messages to stdout")

(options, args) = parser.parse_args()

inline_scripts = []
inline_styles = []
eval_statements = []
everything_else = []
data_violations = []

def print_entry(entry):
    # print ("=========== Report Found =============")
    # print ("{0}: {1}".format(entry['violated-directive'], entry['blocked-uri'][:40]))

    print ("  == entry begin ========= ")
    print ("violated-directive: " + entry['violated-directive'])
    if 'effective-directive' in entry:
        print ("effective-directive: " + entry['effective-directive'])
    if 'referrer' in entry:
        print ("referrer: " + entry['referrer'])
    if 'status-code' in entry:
        print ("status-code: " + entry['status-code'])

    print ("Blocked URI: " + entry['blocked-uri'])
    if 'source-file' in entry:
        print ("source-file: " + entry['source-file'])
    if 'line-number' in entry:
        print ("line-number: " + str(entry['line-number']))
    if 'column-number' in entry:
        print ("column-number: " + str(entry['column-number']))

    print ("document-uri: " + entry['document-uri'])
    print ("original-policy: " + entry['original-policy'])
    print ("  == entry end ========= ")


with open(sys.argv[1], "rb") as logfile:
    freader = io.FlowReader(logfile)
    try:
        s = freader.stream()
        for f in s:
            if f.request.path == "/cspscannerreport" :
                rcontent = f.request.content
                jreport = json.loads(rcontent)['csp-report']
 
                if jreport['blocked-uri'] == 'inline' and jreport['violated-directive'] == 'script-src':
                    if options.inline_scripts and not rcontent in inline_scripts:
                        inline_scripts.append(rcontent)
 
                elif jreport['blocked-uri'] == 'inline' and jreport['violated-directive'] == 'style-src':
                    if options.inline_styles and not rcontent in inline_styles:
                        inline_styles.append(rcontent)

                elif jreport['blocked-uri'] == 'eval': # and jreport['violated-directive'] == 'style-src':
                    if options.eval_statements and not rcontent in eval_statements:
                        eval_statements.append(rcontent)

                elif jreport['blocked-uri'] == 'data': # and jreport['violated-directive'] == 'style-src':
                    if options.data_violations and not rcontent in data_violations:
                        data_violations.append(rcontent)

                elif options.everything_else and not rcontent in everything_else:
                    everything_else.append(rcontent)
        s.close()

    except FlowReadException as e:
        print("Flow file corrupted: {}".format(e))

    if options.inline_scripts:
        print ("===============================")
        print ("== Inline Scripts            ==")
        print ("===============================")
        for rcontent in inline_scripts:
            jreport = json.loads(rcontent)['csp-report']
            # print_entry (jreport)
            if 'line-number' in jreport:
                print ("({0}:{1}): {2}".format(str(jreport['line-number']),str(jreport['column-number']),jreport['document-uri']))
            else:
                print ("(): {0}".format(jreport['document-uri']))

    if options.inline_styles:
        print ("===============================")
        print ("== Inline Styles             ==")
        print ("===============================")
        for rcontent in inline_styles:
            jreport = json.loads(rcontent)['csp-report']
            if 'line-number' in jreport:
                print ("({0}:{1}): {2}".format(str(jreport['line-number']),str(jreport['column-number']),jreport['document-uri']))
            else:
                print ("(): {0}".format(jreport['document-uri']))

    if options.eval_statements:
        print ("===============================")
        print ("== Eval statements           ==")
        print ("===============================")
        for rcontent in eval_statements:
            jreport = json.loads(rcontent)['csp-report']
            entry = jreport
            if 'source-file' in entry:
                print ("{0}:({1}:{2}): {3}".format(entry['violated-directive'], str(jreport['line-number']),str(jreport['column-number']),jreport['source-file']))
            else:
                print ("{0} - document-uri: {1} ".format(entry['violated-directive'], entry['document-uri']))

    if options.data_violations:
        print ("===============================")
        print ("== Data violations           ==")
        print ("===============================")
        for rcontent in data_violations:
            jreport = json.loads(rcontent)['csp-report']
            entry = jreport
            if 'source-file' in entry:
                print ("{0} - source-file: {1} ".format(entry['violated-directive'], entry['source-file']))
            else:
                print ("{0} - document-uri: {1} ".format(entry['violated-directive'], entry['document-uri']))
            print_entry(entry)

    if options.everything_else:
        print ("===============================")
        print ("== Everything else           ==")
        print ("===============================")
        for rcontent in everything_else:
            jreport = json.loads(rcontent)['csp-report']
            print_entry(jreport)
            # print (jreport['violated-directive'])
            # print (jreport)

