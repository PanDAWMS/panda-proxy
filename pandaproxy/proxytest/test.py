# $ source /data/atlpan/srv/etc/sysconfig/panda_proxy-sysconfig
# $ python /data/atlpan/srv/lib/python*/site-packages/pandaproxy/proxytest/test.py

import os
import requests

# key registeration : used by only the panda server
ca_certs='/etc/pki/tls/certs/CERN-bundle.pem'
key_file=os.environ['X509_USER_PROXY']
cert_file=os.environ['X509_USER_PROXY']

pandaID = 123
proxyURL = os.environ['PANDA_URL_SSL']
data = {'pandaID':pandaID}
res = requests.post(proxyURL+'/insertSecretKeyForPandaID',
                    data=data,
                    verify=ca_certs,
                    cert=(cert_file,key_file))
print res.status_code
tmpDict = res.json()
print tmpDict
secretKey = tmpDict['secretKey']


###############################################
#
# communication of the pilot with panda proxy


# get event ranges 
proxyURL = os.environ['PANDA_URL']
data = {'pandaID':pandaID,
        'jobsetID':pandaID+1,
        'secretKey':secretKey,
        'baseURL':'https://aipanda007.cern.ch:25443/server/panda'}
res = requests.post(proxyURL+'/getEventRanges',data)
import cgi
print cgi.parse_qs(res.text.encode('ascii'))


# update event range
data = {'eventRangeID':'0-'+str(pandaID)+'-1-2-3-4',
        'secretKey':secretKey,
        'eventStatus':'finished',
        'baseURL':'https://aipanda007.cern.ch:25443/server/panda'}
res = requests.post(proxyURL+'/updateEventRange',data)
print res.text.encode('ascii')

# get key-pair
data = {'pandaID':pandaID,
        'publicKeyName':'BNL_ObjectStoreKey.pub',
        'privateKeyName':'BNL_ObjectStoreKey',
        'secretKey':secretKey,
        'baseURL':'https://aipanda007.cern.ch:25443/server/panda'}
res = requests.post(proxyURL+'/getKeyPair',data)
tmpDict = cgi.parse_qs(res.text.encode('ascii'))
print tmpDict

privateKey = tmpDict['privateKey']
publicKey  = tmpDict['publicKey']

# upload file
data = {'pandaID':pandaID,
        'secretKey':secretKey,
        'publicKey':publicKey,
        'privateKey':privateKey,
        'baseURL':'http://cephgw.usatlas.bnl.gov:8443/pandaproxytest2/khotest3'}
files = {'uploadFile':('testFile',open('favicon.ico','rb'))}
res = requests.post(proxyURL+'/testIF',data=data,files=files)
print res.text
