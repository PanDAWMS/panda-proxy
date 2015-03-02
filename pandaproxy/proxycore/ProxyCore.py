# core

import Connection

class ProxyCore:

    # constructor
    def __init__(self):
        self.conn = Connection.Connection()


        
    # insert secret key
    def insertSecretKey(self,attribute,secretKey):
        return self.conn.set(attribute,secretKey)


    
    # check secret key for PandaID
    def checkSecretKey(self,attribute,secretKey):
        return secretKey == self.conn.get(attribute)



    # insert secretKey list
    def insertSecretKeyList(self,attributes,secretKey):
        keyVals = []
        for attribute in attributes:
            keyVals.append((attribute,secretKey))
        return self.conn.bulkSet(keyVals)
