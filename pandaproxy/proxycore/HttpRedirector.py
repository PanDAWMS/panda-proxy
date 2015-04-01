# redirect request after key check

import os
import sys
import urlparse
import requests
from proxyconfig import proxy_config


class HttpRedirector:

    # constructor
    def __init__(self):
        from proxycore.ProxyCore import proxyCore
        self.proxyCore = proxyCore
        # remote host config
        self.remoteHostConfig = {}
        # setup remote host config
        self.setupRemoteHostConfig()
                           


    # redirect request
    def redirect(self,attribute,secretKey,baseURL,data):
        # return code
        # 0 : succeeded
        # 1 : access to remote host is disallowed
        # 2 : wrong key
        # 3 : bad response from remote host
        # 4 : unsupported protocol
        # 5 : internal server error
        try:
            # parse URL
            url = urlparse.urlparse(baseURL)
            hostName = url.netloc
            # check host
            if not hostName in self.remoteHostConfig:
                return 1,"access to {0} is not allowed".format(hostName)
            # check secret key
            if not self.proxyCore.checkSecretKey(attribute,secretKey):
                return 2,"wrong key"
            # redirect
            if url.scheme == 'https':
                # get config
                cfg = self.remoteHostConfig[hostName]
                # make connection
                ca_certs=cfg['ca_certs']
                key_file=cfg['key_file']
                cert_file=cfg['cert_file']
                # request
                res = requests.post(baseURL,
                                    data=data,
                                    verify=ca_certs,
                                    cert=(cert_file,key_file))
                if res.status_code == 200:
                    retCode = 0
                else:
                    retCode = 3
                return retCode,res.text.encode('ascii')
            else:
                return 4,"unsupported protocol : {0}".format(url.scheme)
        except:
            errType,errValue = sys.exc_info()[:2]
            return 5,"internal server error {0}:{1}".format(errType,errValue)



    # setup config for remote hosts
    def setupRemoteHostConfig(self):
        try:
            envTag = 'env:'
            # loop over all config strings
            for configStr in proxy_config.http.hostConfig.split(';'):
                items = configStr.split(',')
                hostNames = items[0].split('|')
                # loop over all hosts
                for hostName in hostNames:
                    self.remoteHostConfig[hostName] = {}
                    for item in items[1:]:
                        mapKey,mapVal = item.split('^')[:2]
                        # take param from environment variable
                        if mapVal.startswith(envTag):
                            mapVal = os.environ[mapVal[len(envTag):]]
                        # append
                        self.remoteHostConfig[hostName][mapKey] = mapVal
        except:
            pass



# singleton
httpRedirector = HttpRedirector()
