import sys

# connection class to DB

# logger
from pandalogger.PandaLogger import PandaLogger
_logger = PandaLogger().getLogger('ProxyConnection')


class ProxyConnection:
    
    # constructor
    def __init__(self):
        import redis
        self.conn = redis.StrictRedis(host='localhost', port=6379, db=0)



    # set
    def set(self,key,val,expire=None):
        try:
            dbgMsg = "setting key={0} val={1} expire={2} ".format(key,val,expire)
            _logger.debug(dbgMsg)
            if expire != None:
                tmpStat = self.conn.setex(key,expire,val)
            else:
                tmpStat = self.conn.set(key,val)
            return tmpStat,''
        except:
            errType,errValue = sys.exc_info()[:2]
            errMsg = "failed to set key={0} val={1} expire={2} ".format(key,val,expire)
            errMsg += "with {0}:{1}".format(errType,errValue)
            _logger.error(errMsg)
            return False,errMsg
            


    # bulk set
    def bulkSet(self,keyVals,expire=None):
        pipe = self.conn.pipeline()
        for key,val in keyVals:
            pipe.set(key,val,ex=expire)
        return pipe.execute()



    # get
    def get(self,key):
        try:
            return True,self.conn.get(key)
        except:
            errType,errValue = sys.exc_info()[:2]
            errMsg = "failed to get value for key={0} ".format(key)
            errMsg += "with {0}:{1}".format(errType,errValue)
            _logger.error(errMsg)
            return False,errMsg



    # bulk get
    def bulkGet(self,keys):
        pipe = self.conn.pipeline()
        for key in keys:
            pipe.get(key)
        return pipe.execute()



# singleton
proxyConnection = ProxyConnection()
