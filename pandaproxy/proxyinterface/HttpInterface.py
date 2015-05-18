import cgi
import sys
import uuid
import json
import urllib
from proxycore import ProxyUtils
from proxycore.HttpRedirector import httpRedirector

# logger
from pandalogger.PandaLogger import PandaLogger
from pandalogger.LogWrapper import LogWrapper
_logger = PandaLogger().getLogger('HttpInterface')
        

# insert secretKey
def insertSecretKeyForPandaID(req,pandaID,secretKey=None):
    logger = LogWrapper(_logger,"insertSecretKeyForPandaID <PandaID={0}>".format(pandaID))
    retDict = {}
    # check permission
    if not ProxyUtils.hasPermission(req):
        msgStr = "permission denied"
        retDict['errorCode'] = 1
        retDict['errorDiag'] = msgStr
        logger.error(msgStr)
        return json.dumps(retDict)
    # generate key
    if secretKey == None:
        secretKey = uuid.uuid4().hex
    # use unicode
    secretKey = unicode(secretKey)
    logger.debug("secretKey={0}".format(secretKey))
    # exec
    try:
        redStat,redOut = httpRedirector.proxyCore.insertSecretKey(pandaID,secretKey)
        if redStat == True:
            msgStr = "done"
            retDict['errorCode'] = 0
            retDict['errorDiag'] = msgStr
            retDict['secretKey'] = secretKey
            logger.debug(msgStr)
            return json.dumps(retDict)
    except:
        errType,errValue = sys.exc_info()[:2]
        redStat = False
        redOut = "{0}:{1}".format(errType,errValue)
    msgStr = "failed with {0}:{1}".format(redStat,redOut)
    retDict['errorCode'] = 2
    retDict['errorDiag'] = msgStr
    logger.error(msgStr)
    return json.dumps(retDict)



# get event ranges
def getEventRanges(req,**kwd):
    logger = LogWrapper(_logger,"getEventRanges <{0}>".format(str(kwd)))
    logger.debug("start")
    # check key words
    chkStat,secretKey,baseURL,newKwd = ProxyUtils.checkKeyWords(kwd)
    if not chkStat:
        errMsg = newKwd
        logger.error(errMsg)
        return "ERROR : "+errMsg
    # check URL
    baseURL += '/getEventRanges'
    # get PandaID
    if not 'pandaID' in newKwd:
        errMsg = "no PandaID"
        logger.error(errMsg)
        return "ERROR : "+errMsg
    # exec
    redStat,redOut = httpRedirector.redirect(newKwd['pandaID'],secretKey,baseURL,newKwd)
    if redStat != 0:
        errMsg = "failed with {0} : {1}".format(redStat,redOut)
        logger.error(errMsg)
        return "ERROR : "+errMsg
    # return
    logger.debug("done with {0}".format(str(redOut)))
    return redOut



# update event range
def updateEventRange(req,**kwd):
    logger = LogWrapper(_logger,"updateEventRange <{0}>".format(str(kwd)))
    logger.debug("start")
    # check key words
    chkStat,secretKey,baseURL,newKwd = ProxyUtils.checkKeyWords(kwd)
    if not chkStat:
        errMsg = newKwd
        logger.error(errMsg)
        return "ERROR : "+errMsg
    # check URL
    baseURL += '/updateEventRange'
    # get eventRangeID
    if not 'eventRangeID' in newKwd:
        errMsg = "no eventRangeID"
        logger.error(errMsg)
        return "ERROR : "+errMsg
    # extract PandaID
    try:
        pandaID = newKwd['eventRangeID'].split('-')[1]
    except:
        errMsg = "failed to extract PandaID from eventRangeID"
        logger.error(errMsg)
        return "ERROR : "+errMsg
    # exec
    redStat,redOut = httpRedirector.redirect(pandaID,secretKey,baseURL,newKwd)
    if redStat != 0:
        errMsg = "failed with {0} : {1}".format(redStat,redOut)
        logger.error(errMsg)
        return "ERROR : "+errMsg
    # return
    logger.debug("done with {0}".format(str(redOut)))
    return redOut



# get key pair
def getKeyPair(req,**kwd):
    logger = LogWrapper(_logger,"getKeyPair <{0}>".format(str(kwd)))
    logger.debug("start")
    # check key words
    chkStat,secretKey,baseURL,newKwd = ProxyUtils.checkKeyWords(kwd)
    if not chkStat:
        errMsg = newKwd
        logger.error(errMsg)
        return "ERROR : "+errMsg
    # check URL
    baseURL += '/getKeyPair'
    # get PandaID
    if not 'pandaID' in newKwd:
        errMsg = "no PandaID"
        logger.error(errMsg)
        return "ERROR : "+errMsg
    pandaID = newKwd['pandaID']
    del newKwd['pandaID']
    # exec
    redStat,redOut = httpRedirector.redirect(pandaID,secretKey,baseURL,newKwd)
    if redStat != 0:
        errMsg = "failed with {0} : {1}".format(redStat,redOut)
        logger.error(errMsg)
        return "ERROR : "+errMsg
    # decode key pair
    try:
        dic = cgi.parse_qs(redOut)
        # use the fisrt entry
        newDict = {}
        for item in dic.keys():
            newDict[item]= dic[item][0]
        dic = newDict
        # replace keys
        for item in ['publicKey','privateKey']:
            nameKey = '{0}Name'.format(item)
            # make key-value
            key = '{0}:{1}'.format(item,newKwd[nameKey])
            value = dic[item]
            # keep in memory
            tmpStat,tmpOut = httpRedirector.proxyCore.insertKeyValue(key,value)
            if not tmpStat:
                errMsg = "failed to keep {0} in memory".format(key)
                logger.error(errMsg)
                return "ERROR : "+errMsg
            # replace keys with memory key
            dic[item] = key
        # encode
        redOut = urllib.urlencode(dic)
    except:
        errType,errValue = sys.exc_info()[:2]
        errMsg = "internal server error {0}:{1}".format(errType,errValue)
        logger.error(errMsg)
        return "ERROR : "+errMsg
    # return
    logger.debug("done with {0}".format(str(redOut)))
    return redOut



# test I/F
def testIF(req,**kwd):
    retStr = ''
    for tmpKey,tmpVal in kwd.iteritems():
        _logger.debug('{0} {1}'.format(tmpKey,str(tmpVal)))
        retStr += 'key={0} val={1}\n'.format(tmpKey,str(tmpVal))
    return retStr
