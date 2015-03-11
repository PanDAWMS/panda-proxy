import uuid
import json
import ProxyUtils
from ProxyRedirector import redirector

# logger
from pandalogger.PandaLogger import PandaLogger
from pandalogger.LogWrapper import LogWrapper
_logger = PandaLogger().getLogger('ProxyInterface')
        

# insert secretKey
def insertSecretKeyForPandaID(req,PandaID,secretKey=None):
    logger = LogWrapper(_logger,"<PandaID={0}>".format(PandaID))
    retDict = {}
    # check permission
    if not ProxyUtils.hasPermission(req):
        msgStr = "permission denied"
        retDict['errorCode'] = 1
        retDict['errorDiag'] = msgStr
        tmpKeys = req.subprocess_env.keys()
        tmpKeys.sort()
        for tmpKey in tmpKeys:
            logger.error("%s %s" % (tmpKey,req.subprocess_env[tmpKey]))
        logger.error(msgStr)
        return json.dumps(retDict)
    # generate key
    if secretKey == None:
        secretKey = uuid.uuid4().hex
    logger.debug("secretKey={0}".format(secretKey))
    # exec
    redStat = redirector.proxyCore.insertSecretKey(PandaID,secretKey)
    if redStat == True:
        msgStr = "done"
        retDict['errorCode'] = 0
        retDict['errorDiag'] = msgStr
        retDict['secretKey'] = secretKey
        logger.debug(msgStr)
        return json.dumps(retDict)
    msgStr = "failed with {0}".format(redStat)
    retDict['errorCode'] = 2
    retDict['errorDiag'] = msgStr
    logger.error(msgStr)
    return json.dumps(retDict)



# get event ranges
def getEventRanges(req,**kwd):
    # check URL
    if not baseURL.endswith('/getEventRanges'):
        return "ERROR : wrong baseURL"
    # check key words
    chkStat,secretKey,baseURL,newKwd = ProxyUtils.checkKeyWords(kwd)
    if not chkStat:
        return "ERROR : "+newKwd
    # get PandaID
    if not 'pandaID' in newKwd:
        return "ERROR : no PandaID"
    # exec
    redStat,redOut = redirector.redirect(newKwd['pandaID'],secretKey,baseURL,newKwd)
    if redStat != 0:
        return "ERROR : failed with {0} : {1}".format(redStat,redOut)
    # return
    return redOut



# update event range
def updateEventRange(req,**kwd):
    # check URL
    if not baseURL.endswith('/updateEventRange'):
        return "ERROR : wrong baseURL"
    # check key words
    chkStat,secretKey,baseURL,newKwd = ProxyUtils.checkKeyWords(kwd)
    if not chkStat:
        return "ERROR : "+newKwd
    # get eventRangeID
    if not 'eventRangeID' in newKwd:
        return "ERROR : no eventRangeID"
    # extract PandaID
    try:
        pandaID = newKwd['eventRangeID'].split('-')[1]
    except:
        return "ERROR : failed to extract PandaID from eventRangeID"
    # exec
    redStat,redOut = redirector.redirect(pandaID,secretKey,baseURL,newKwd)
    if redStat != 0:
        return "ERROR : failed with {0} : {1}".format(redStat,redOut)
    # return
    return redOut
