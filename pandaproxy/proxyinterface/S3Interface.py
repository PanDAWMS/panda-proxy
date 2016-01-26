import sys
import json
import InterfaceUtils
from proxycore import ProxyUtils
from proxycore.ProxyCore import proxyCore
from proxycore.S3Redirector import s3Redirector
from proxycore.PandaCache import pandaCache


# logger
from pandalogger.PandaLogger import PandaLogger
from pandalogger.LogWrapper import LogWrapper
_logger = PandaLogger().getLogger('S3Interface')



# check if there are parameters to access to ObjectStore
def checkS3KeyWords(kwd,https=False):
    # check key words
    chkStat,secretKey,url,newKwd = ProxyUtils.checkKeyWords(kwd,https=https)
    if not chkStat:
        errMsg = newKwd
        return False,None,None,errMsg
    # get PandaID
    if not https:
        if not 'pandaID' in newKwd:
            return False,None,None,"no PandaID"
        pandaID = newKwd['pandaID']
        del newKwd['pandaID']
    # check key-pairs
    for tmpKey in ['publicKey','privateKey']:
        if not tmpKey in newKwd:
            return False,None,None,"{0} is not given".format(tmpKey)
    # check secret key
    if not https:
        if not proxyCore.checkSecretKey(pandaID,secretKey):
            return False,None,None,"wrong key"
    return True,url,newKwd,""



# get file info
def getFileInfo(req, **kwd):
    logger = LogWrapper(_logger,"<getFileInfo>")
    # check key words
    tmpState,url,newKwd,errMsg = checkS3KeyWords(kwd)
    if not tmpState:
        logger.error(errMsg)
        return InterfaceUtils.makeResponse(10,"ERROR : "+errMsg)
    try:
        ret = s3Redirector.getFileInfo(url, newKwd['privateKey'], newKwd['publicKey'])
        return InterfaceUtils.makeResponse(0,"OK",{'fileInfo':json.dumps(ret)})
    except:
        errType,errValue = sys.exc_info()[:2]
        errMsg = "internal server error {0}:{1}".format(errType,errValue)
        logger.error(errMsg)
        return InterfaceUtils.makeResponse(10,"ERROR : "+errMsg)



# upload file
def setFileToS3(req, **kwd):
    logger = LogWrapper(_logger,"<setFileToS3>")
    # check key words
    tmpState,url,newKwd,errMsg = checkS3KeyWords(kwd)
    if not tmpState:
        logger.error(errMsg)
        return InterfaceUtils.makeResponse(10,"ERROR : "+errMsg)
    # check params
    if not 'uploadFile' in newKwd:
        errMsg = "no uploadFile"
        logger.error(errMsg)
        return InterfaceUtils.makeResponse(10,"ERROR : "+errMsg)
    fileSize = None
    if 'fileSize' in newKwd:
        fileSize = newKwd['fileSize']
    fileChecksum = None
    if 'fileChecksum' in newKwd:
        fileChecksum = newKwd['fileChecksum']
    try:
        tmpStat,errMsg = s3Redirector.setFileContentToS3(newKwd['uploadFile'].file.read(),
                                                         url,
                                                         newKwd['privateKey'],
                                                         newKwd['publicKey'],
                                                         fileSize,
                                                         fileChecksum)
        if not tmpStat:
            logger.error(errMsg)
            return InterfaceUtils.makeResponse(10,"ERROR : "+errMsg)
        return InterfaceUtils.makeResponse(0,"OK")
    except:
        errType,errValue = sys.exc_info()[:2]
        errMsg = "internal server error {0}:{1}".format(errType,errValue)
        logger.error(errMsg)
        return InterfaceUtils.makeResponse(10,"ERROR : "+errMsg)



# download file contents
def getFileContent(req, **kwd):
    logger = LogWrapper(_logger,"<getFileContent>")
    # check key words
    tmpState,url,newKwd,errMsg = checkS3KeyWords(kwd)
    if not tmpState:
        logger.error(errMsg)
        return "ERROR : "+errMsg
    try:
        ret = s3Redirector.getFileContent(url, newKwd['privateKey'], newKwd['publicKey'])
        return ret
    except:
        errType,errValue = sys.exc_info()[:2]
        errMsg = "internal server error {0}:{1}".format(errType,errValue)
        logger.error(errMsg)
        return "ERROR : "+errMsg



# get pre-signed URL
def getPresignedURL(req, **kwd):
    logger = LogWrapper(_logger,"<getFileInfo>")
    # check for HTTPS
    tmpState,errMsg = checkPermissionHTTPS(req)
    if tmpState == False:
        logger.error(errMsg)
        return InterfaceUtils.makeResponse(10,"ERROR : "+errMsg)
    # authorized with HTTPS
    if tmpState == True:
        https = True
    else:
        https = False
    # check key words
    tmpState,url,newKwd,errMsg = checkS3KeyWords(kwd,https)
    if not tmpState:
        logger.error(errMsg)
        return InterfaceUtils.makeResponse(10,"ERROR : "+errMsg)
    # method
    if 'method' in newKwd:
        method = newKwd['method']
    else:
        method = 'PUT'
    try:
        tmpStat,errMsg,ret = s3Redirector.getPresignedURL(url,newKwd['privateKey'],newKwd['publicKey'],method)
        if not tmpStat:
            logger.error(errMsg)
            return InterfaceUtils.makeResponse(10,"ERROR : "+errMsg)
        return InterfaceUtils.makeResponse(0,"OK",{'presignedURL':ret})
    except:
        errType,errValue = sys.exc_info()[:2]
        errMsg = "internal server error {0}:{1}".format(errType,errValue)
        logger.error(errMsg)
        return InterfaceUtils.makeResponse(10,"ERROR : "+errMsg)



# check permission for HTTPS
def checkPermissionHTTPS(req):
    # no SSL
    if not 'SSL_CLIENT_S_DN' in req.subprocess_env:
        # not applicable
        return None,None
    # get DN
    dn = req.subprocess_env['SSL_CLIENT_S_DN']
    # get DN list
    tmpStat,dnList = pandaCache.getDNsForS3()
    if not tmpStat:
        return False,'Failed to get authorized DN list'
    # loop over all DNs
    for tmpDN in dnList:
        if tmpDN in dn:
            return True,None
    return False,'Authorization failure'

