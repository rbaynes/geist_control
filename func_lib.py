#!/usr/bin/env python3

# Common local function library for python (3).
# rbaynes 2017-12-11  

import sys, os, requests, json

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
    return resp


#------------------------------------------------------------------------------
# Get the average wattage used by this outlet.
def get_watts( IP, DID, outlet ):
    log.debug( "Getting wattage for outlet %s" % ( outlet ))
    resp = get( IP, '/api/dev/' + DID + '/outlet/' + outlet + '/measurement/3/value' )
    return resp


