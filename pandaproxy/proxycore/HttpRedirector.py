# redirect request after key check

import os
import sys
import urlparse
import requests


class HttpRedirector:

    # constructor
    def __init__(self):
        from proxycore.ProxyCore import proxyCore
        self.proxyCore = proxyCore
        # remote host config
        # FIXME read from cfg
        self.remoteHostConfig = {
            'aipanda007.cern.ch:25443' : {
                'ca_certs'  : '/etc/pki/tls/certs/CERN-bundle.pem',
                'key_file'  : os.environ['X509_USER_PROXY'],
                'cert_file' : os.environ['X509_USER_PROXY'],
                },
            'pandaserver.cern.ch:25443' : {
                'ca_certs'  : '/etc/pki/tls/certs/CERN-bundle.pem',
                'key_file'  : os.environ['X509_USER_PROXY'],
                'cert_file' : os.environ['X509_USER_PROXY'],
                },
            }
                           


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



# singleton
httpRedirector = HttpRedirector()
