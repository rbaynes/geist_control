#!/usr/bin/env python3
#
# rbaynes 2017-10-03  
# Script to get the average wattage used by an outlet on a Geist IP addressable 
# power strip using its REST JSON API.
#
# Installation:
#   sudo apt-get install -y python3
#   pip install --upgrade virtualenv
#   virtualenv --python python3 env
#   source env/bin/activate
#   pip install requests
# 
# http://www.geistglobal.com/sites/all/files/site/User_Manuals/Power/gm1174_-_r-series_v4_pdu_rev3.0.pdf
#
# https://wiki.openag.media.mit.edu/users/rbaynes/notes/geistpdu
#
import sys, os, getopt, argparse
from func_lib import log, get, getDID, post, get_watts


#------------------------------------------------------------------------------
# Entry point for the script
def main():

    # glorious command line args
    parser = argparse.ArgumentParser(description='cmd line args')
    parser.add_argument('--IP', required=True, type=str, \
                        help='IP address of strip')
    parser.add_argument('--outlet', required=True, type=str, \
                        help='Outlet number 1-4')
    parser.add_argument('--csv', dest='csv', \
                        action='store_true', help='output CSV: <IP>,<outlet>,<watts>')
    parser.add_argument('--debug', dest='debug', \
                        action='store_true', help='enable debug logging')
    args = parser.parse_args()

    # enable debug logging if set on cmd line
    if( args.debug ):
        log.enableDebug() 

    # outlet is 0-3 in Geist API and 1-4 printed on strip 
    # We take as input 1-4, so validate and convert
    if args.outlet not in ['1', '2', '3', '4']:
        log.fatal( "--outlet valid values are 1-4" )
    outlet = str( int( args.outlet ) - 1 )

    try:
        # automatically get device ID
        log.debug( "Getting device ID..." )
        DID = getDID( args.IP )
        log.debug( "DID=%s" % DID)

        # finally, do what the user wants.
        watts = get_watts( args.IP, DID, outlet )
        if args.csv:
            print( "%s,%s,%s" % ( args.IP, args.outlet, watts['data'] ))
        else:
            print( "Strip %s Outlet %s is using %s watts." % 
                ( args.IP, args.outlet, watts['data'] ))
    except Exception as e:
        #print( "ERROR: Exception: %s" % e)
        print( "ERROR reaching %s" % args.IP )
        exit( 1 )


#------------------------------------------------------------------------------
if __name__ == "__main__":
    main()


