#!/usr/bin/env python3
#
# rbaynes 2017-10-03  
# Script to control a Geist IP addressable power strip using its 
# REST JSON API.
#
# Installation:
# 1. sudo apt-get install -y python3.5
# 2. sudo pip install requests
# 
# http://www.geistglobal.com/sites/all/files/site/User_Manuals/Power/gm1174_-_r-series_v4_pdu_rev3.0.pdf
#
# https://wiki.openag.media.mit.edu/users/rbaynes/notes/geistpdu
#
import sys, os, getopt, argparse, requests, json

#------------------------------------------------------------------------------
class log(object):

    # static (also called class) variables, private (mangled) by name __
    __debug_msg = False
    __file_name = "error.txt"
    __file_handle = None

    @staticmethod
    def enableDebug():
        log.__debug_msg = True

    @staticmethod
    def open( fn ):
        log.__file_name = fn
        log.open()

    @staticmethod
    def open():
        log.__file_handle = open( log.__file_name, 'w' )

    @staticmethod
    def write( str ):
        print( str )
        if( log.__file_handle is not None ):
            log.__file_handle.write( "%s\n" % str )

    @staticmethod
    def fatal( str ):
        log.write( "FATAL: %s" % str )
        sys.exit(2)

    @staticmethod
    def error( str ):
        log.write( "ERROR: %s" % str )

    @staticmethod
    def warn( str ):
        msg = "WARN: %s" % str
        log.write( msg )

    @staticmethod
    def debug( str ):
        if( not log.__debug_msg ):
            return
        log.write( "DEBUG: %s" % str )

    @staticmethod
    def info( str ):
        log.write( str )


#------------------------------------------------------------------------------
# Return the JSON response of a GET request to this URL.
def get( IP, path ):
    URL = 'http://' + IP + path
    log.debug( 'Getting %s ' % URL )
    resp = requests.get( URL )
    if resp.status_code != 200:
        log.fatal( 'HTTP request of %s failed with code %d' % \
                 ( URL, resp.status_code ))
    return resp.json()


#------------------------------------------------------------------------------
# Get the device ID from the strip.
def getDID( IP ):
    resp = get( IP, '/api/dev' )
    rdata = resp['data']
    dkeys = rdata.keys()
    keyList = list( dkeys )
    did = keyList[0]
    return did


#------------------------------------------------------------------------------
# POST some JSON data to the REST API and return the JSON response.
def post( IP, path, data ):
    URL = 'http://' + IP + path
    log.debug( 'Posting %s with %s' % ( URL, data ))
    resp = requests.post( URL, json=data )
    if resp.status_code != 200:
        log.fatal( 'HTTP POST to %s with %s failed with code %d' % \
                 ( URL, data, resp.status_code ))
    return resp.json()


#------------------------------------------------------------------------------
# Login to the strip and return an auth token.
def login( IP, username, password ):
    # create out JSON data object for the POST to the API
    data = {"token":"","cmd":"login","data":{"password":password}}
    resp = post( IP, '/api/auth/' + username, data )
    rdata = resp['data']
    authToken = rdata['token']
    return authToken


#------------------------------------------------------------------------------
# Outlet control
def outlet( IP, DID, AuthToken, outlet, action ):
    log.debug( "Turning outlet %s %s" % ( outlet, action ))
    # create out JSON data object for the POST to the API
    data = {"token":AuthToken,"cmd":"control","data":{"action":action}}
    resp = post( IP, '/api/dev/' + DID + '/outlet/' + outlet, data )


#------------------------------------------------------------------------------
# Entry point for the script
def main():

    # glorious command line args
    parser = argparse.ArgumentParser(description='cmd line args')
    parser.add_argument('--IP', required=True, type=str, \
                        help='IP address of strip')
    parser.add_argument('--outlet', required=True, type=str, \
                        help='Outlet number 1-4')
    parser.add_argument('--action', required=True, type=str, \
                        help='Action: on/off/reboot')
    parser.add_argument('--username', type=str, default='admin', \
                        help='Default username is "admin"')
    parser.add_argument('--password', type=str, default='admin', \
                        help='Default password is "admin"')
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
    args.outlet = str( int( args.outlet ) - 1 )

    # automatically get device ID
    log.debug( "Getting device ID..." )
    DID = getDID( args.IP )
    log.debug( "DID=%s" % DID)

    # login and get auth token
    log.debug( "Logging in to get auth token..." )
    AuthToken = login( args.IP, args.username, args.password )
    log.debug( "AuthToken=%s" % AuthToken)

    # finally, do what the user wants.
    outlet( args.IP, DID, AuthToken, args.outlet, args.action )


#------------------------------------------------------------------------------
if __name__ == "__main__":
    main()


