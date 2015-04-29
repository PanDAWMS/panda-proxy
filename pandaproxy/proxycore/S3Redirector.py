import sys
import urlparse
import boto
import boto.s3.connection
import boto.s3.key 

# logger
from pandalogger.PandaLogger import PandaLogger
from pandalogger.LogWrapper import LogWrapper
_logger = PandaLogger().getLogger('S3Redirector')



class S3Redirector:
    # constructor
    def __init__(self):
        from proxycore.ProxyCore import proxyCore
        self.proxyCore = proxyCore


    def getKey(self, url, privateKey, publicKey, existed=False):
        #
	# url format: http://hostname:port/bucketname/filename
        # bucketname can't contain UPPER charater 
        #
        # extract hostname, port, buckname and filename(key) from url
        parsed = urlparse.urlparse(url)
        hostname = parsed.netloc.partition(':')[0]
        port = int(parsed.netloc.partition(':')[2])
        path = parsed.path.strip("/")
        index = path.index("/")
        bucket_name = path[:index]
        key_name = path[index+1:]
        # get key-pairs from Memory
        tmpStat,access_key = self.proxyCore.getValue(publicKey)
        tmpStat,secret_key = self.proxyCore.getValue(privateKey)
        # connect to s3
        self.__connect = boto.connect_s3(
            aws_access_key_id = access_key,
            aws_secret_access_key = secret_key,
            host = hostname,
            port = port,
            is_secure=False,
            calling_format = boto.s3.connection.OrdinaryCallingFormat(),
            )
        if not existed:
            # create a new bucket and key
            bucket = self.__connect.create_bucket(bucket_name)    
            key = boto.s3.key.Key(bucket, key_name)
        else:
            # get existed bucket with key
            bucket = self.__connect.get_bucket(bucket_name)
            key = bucket.get_key(key_name)
        return key


    def getFileInfo(self, url, privateKey, publicKey):
        key = self.getKey(url, privateKey, publicKey, existed=True)
        md5 = key.get_metadata("md5")
        return key.size, md5


    def setFileContentToS3(self, fileData, destination, privateKey, publicKey, 
                           fileSize=None, fileChecksum=None):
        #
        # fileData: string of file contents
        # destination: url with this format: http://hostname:port/bucketname/filename
        # bucketname can't contain UPPER charater 
        #
        logger = LogWrapper(_logger,"<setFileContentToS3>")
        try:
            logger.debug(1)
            key = self.getKey(destination, privateKey, publicKey)
            if key == None:
                return False, "Failed to find the key on the dstination: %s" % destination
            # set file (and md5) to s3
            logger.debug(2)
            if fileChecksum:
                key.set_metadata("md5", fileChecksum)
            logger.debug(3)
            size = key.set_contents_from_string(fileData)
            logger.debug(4)
	    # check size
            if fileSize and str(fileSize) != str(key.size):
                return False, "File size(%s) does not matched with remote size(%s)" % (fileSize, key.size)
            # check md5 
            if fileChecksum and fileChecksum != key.md5:
                return False, "Flie checksum(%s) does not matched with remote checksum(%s)" % (fileChecksum, key.md5)
            logger.debug(5)
        except:
            errType,errValue = sys.exc_info()[:2]
            errMsg = "failed to upload with {0}:{1}".format(errType,errValue)
            return False, errMsg
        return True, None


    def getFileContent(self, url, privateKey, publicKey):
        # for test get the content in the file
        key = self.getKey(url, privateKey, publicKey, existed=True)
        content = key.get_contents_as_string()
        return content



# singleton
s3Redirector = S3Redirector()
