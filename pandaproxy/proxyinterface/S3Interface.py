import sys
import json
from proxycore import ProxyUtils
from proxycore.ProxyCore import proxyCore
from proxycore.S3Redirector import s3Redirector


# logger
from pandalogger.PandaLogger import PandaLogger
from pandalogger.LogWrapper import LogWrapper
_logger = PandaLogger().getLogger('S3Interface')



# check if there are parameters to access to ObjectStore
def checkS3KeyWords(kwd):
    # check key words
    chkStat,secretKey,url,newKwd = ProxyUtils.checkKeyWords(kwd)
    if not chkStat:
        errMsg = newKwd
        return False,None,None,errMsg
    # get PandaID
    if not 'pandaID' in newKwd:
        return False,None,None,"no PandaID"
    pandaID = newKwd['pandaID']
    del newKwd['pandaID']
    # check key-pairs
    for tmpKey in ['publicKey','privateKey']:
        if not tmpKey in newKwd:
            return False,None,None,"{0} is not given".format(tmpKey)
    # check secret key
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
        return "ERROR : "+errMsg
    try:
        ret = s3Redirector.getFileInfo(url, newKwd['privateKey'], newKwd['publicKey'])
        return json.dumps(ret)
    except:
        errType,errValue = sys.exc_info()[:2]
        errMsg = "internal server error {0}:{1}".format(errType,errValue)
        logger.error(errMsg)
        return "ERROR : "+errMsg



# upload file
def setFileToS3(req, **kwd):
    logger = LogWrapper(_logger,"<setFileToS3>")
    # check key words
    tmpState,url,newKwd,errMsg = checkS3KeyWords(kwd)
    if not tmpState:
        logger.error(errMsg)
        return "ERROR : "+errMsg
    # check params
    if not 'uploadFile' in newKwd:
        errMsg = "no uploadFile"
        logger.error(errMsg)
        return "ERROR : "+errMsg
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
            return "ERROR : "+errMsg
        return "OK"
    except:
        errType,errValue = sys.exc_info()[:2]
        errMsg = "internal server error {0}:{1}".format(errType,errValue)
        logger.error(errMsg)
        return "ERROR : "+errMsg



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
