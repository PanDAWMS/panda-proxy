# core

class ProxyCore:

    # constructor
    def __init__(self):
        from ProxyConnection import proxyConnection
        self.conn = proxyConnection



    # get access key from PandaID
    def getKeyFromPandaID(self,pandaID):
        return 'PandaID:{0}'.format(pandaID)



    # insert secret key
    def insertSecretKey(self,pandaID,secretKey,expire=None):
        if expire == None:
            expire = 7*24*60*60
        attribute = self.getKeyFromPandaID(pandaID)
        return self.conn.set(attribute,secretKey,expire=expire)


    
    # check secret key for PandaID
    def checkSecretKey(self,pandaID,secretKey):
        attribute = self.getKeyFromPandaID(pandaID)
        tmpStat,keyInMemory = self.conn.get(attribute)
        if not tmpStat:
            return False
        return secretKey == keyInMemory



    # insert secretKey list
    def insertSecretKeyList(self,attributes,secretKey,expire=None):
        if expire == None:
            expire = 7*24*60*60
        keyVals = []
        for attribute in attributes:
            keyVals.append((attribute,secretKey))
        return self.conn.bulkSet(keyVals,expire=expire)



    # general method to insert key-value
    def insertKeyValue(self,key,value,expire=None):
        return self.conn.set(key,value,expire=expire)



    # general method to get value
    def getValue(self,key):
        return self.conn.get(key)



# singleton
proxyCore = ProxyCore()
