import ProxyUtils
from ProxyRedirector import redirector

# logger
from pandalogger.PandaLogger import PandaLogger
_logger = PandaLogger().getLogger('ProxyInterface')
        

# insert secretKey
def insertSecretKeyForPandaID(req,PandaID,secretKey):
    # check permission
    if not ProxyUtils.hasPermission(req):
        return "ERROR : permission denied"
    _logger.debug("aaaa 2")
    # exec
    redStat = redirector.proxyCore.insertSecretKey(PandaID,secretKey)
    if redStat == True:
        return "SUCCEEDED"
    return "ERROR : failed"



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
