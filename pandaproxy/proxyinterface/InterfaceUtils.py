import urllib

# make response
def makeResponse(errorCode,errorMsg,msgData=None):
    tmpDict = {'StatusCode':errorCode,
               'ErrorMsg':errorMsg}
    if msgData != None:
        for tmpKey,tmpVal in msgData.iteritems():
            tmpDict[tmpKey] = tmpVal
    return urllib.urlencode(tmpDict)
    
