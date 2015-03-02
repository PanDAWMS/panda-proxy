#!/usr/bin/python

"""
entry point
"""

import sys
import cgi

from proxycore.Utils import DummyReq


# import web I/F
allowedMethods = []

from proxycore.ProxyInterface import insertSecretKeyForPandaID,getEventRanges,updateEventRange
allowedMethods += ['insertSecretKeyForPandaID','getEventRanges','updateEventRange']


# application
def application(environ, start_response):
    # get method name
    methodName = ''
    if environ.has_key('SCRIPT_NAME'):
        methodName = environ['SCRIPT_NAME'].split('/')[-1]
    # check method name    
    if not methodName in allowedMethods:
        exeRes = "False : %s is forbidden" % methodName
    else:
        # get method object
        tmpMethod = None
        try:
            exec "tmpMethod = %s" % methodName
        except:
            pass
        # object not found
        if tmpMethod == None:
            exeRes = "False"
        else:
            # get params 
            tmpPars = cgi.FieldStorage(environ['wsgi.input'], environ=environ,
                                       keep_blank_values=1)
            # convert to map
            params = {}
            for tmpKey in tmpPars.keys():
                if tmpPars[tmpKey].file != None and tmpPars[tmpKey].filename != None:
                    # file
                    params[tmpKey] = tmpPars[tmpKey]
                else:
                    # string
                    params[tmpKey] = tmpPars.getfirst(tmpKey)
            # dummy request object
            dummyReq = DummyReq(environ)
            try:
                # exec
                exeRes = apply(tmpMethod,[dummyReq],params)
                # convert bool to string
                if exeRes in [True,False]:
                    exeRes = str(exeRes)
            except:
                errType,errValue = sys.exc_info()[:2]
                errStr = ""
                for tmpKey,tmpVal in environ.iteritems():
                    errStr += "%s : %s\n" % (tmpKey,str(tmpVal))
                # return internal server error
                start_response('500 INTERNAL SERVER ERROR', [('Content-Type', 'text/plain')]) 
                return ["%s %s" % (errType,errValue)]
    # return
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [exeRes]

