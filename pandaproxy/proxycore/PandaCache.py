import sys
import requests
from proxyconfig import proxy_config


# logger
from pandalogger.PandaLogger import PandaLogger
from pandalogger.LogWrapper import LogWrapper
_logger = PandaLogger().getLogger('PandaCache')



class PandaCache:
    # constructor
    def __init__(self):
        from proxycore.ProxyCore import proxyCore
        self.proxyCore = proxyCore



    # get DNs authorized for S3 access
    def getDNsForS3(self):
        try:
            logger = LogWrapper(_logger,"<getDNsForS3>")
            # key for redis
            keyName = "DNsForS3"
            # get DNs
            rawTxt = ''
            tmpStat,dnList = self.proxyCore.getValue(keyName)
            if tmpStat and dnList != None:
                return True,dnList
            # get DNs from Panda
            logger.debug('getting DNs')
            baseURL = 'http://{0}:{1}/server/panda/getDNsForS3'.format(proxy_config.panda.pserveralias,
                                                                       proxy_config.panda.pserverporthttp)
            res = requests.get(baseURL)
            rawTxt = res.text
            res.raise_for_status()
            # decode
            dnList = res.json()
            logger.debug('got {0}'.format(str(dnList)))
            # insert
            self.proxyCore.insertKeyValue(keyName,dnList,60*10)
            # return
            return True,dnList
        except:
            errType,errValue = sys.exc_info()[:2]
            errMsg = "internal server error {0}:{1}".format(errType,errValue)
            logger.error(errMsg)
            return False,None



# singleton
pandaCache = PandaCache()
