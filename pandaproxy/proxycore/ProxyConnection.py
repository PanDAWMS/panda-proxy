# connection class to DB

class Connection:
    
    # constructor
    def __init__(self):
        import redis
        self.conn = redis.StrictRedis(host='localhost', port=6379, db=0)



    # set
    def set(self,key,val):
        return self.conn.set(key,val)



    # bulk set
    def bulkSet(self,keyVals):
        pipe = self.conn.pipeline()
        for key,val in keyVals:
            pipe.set(key,val)
        return pipe.execute()



    # get
    def get(self,key):
        return self.conn.get(key)



    # bulk get
    def bulkGet(self,keys):
        pipe = self.conn.pipeline()
        for key in keys:
            pipe.get(key)
        return pipe.execute()
