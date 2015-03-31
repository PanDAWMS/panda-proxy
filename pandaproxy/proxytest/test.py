# $ source /data/atlpan/srv/etc/sysconfig/panda_proxy-sysconfig
# $ python /data/atlpan/srv/lib/python*/site-packages/pandaproxy/proxytest/test.py

import os
import urllib3

# key registeration : used by only the panda server
http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs='/etc/grid-security/certificates/CERN-Root-2.pem',
    key_file=os.environ['X509_USER_PROXY'],
    cert_file=os.environ['X509_USER_PROXY']
    )
pandaID = 123
proxyURL = os.environ['PANDA_URL_SSL']
data = {'pandaID':pandaID}
res = http.request('POST',proxyURL+'/insertSecretKeyForPandaID',data)
print res.status
import json
tmpDict = json.loads(res.data)
print tmpDict
secretKey = tmpDict['secretKey']


# get event ranges 
http = urllib3.PoolManager()
proxyURL = os.environ['PANDA_URL']
data = {'pandaID':pandaID,
        'jobsetID':pandaID+1,
        'secretKey':secretKey,
        'baseURL':'https://aipanda007.cern.ch:25443/server/panda'}
res = http.request('POST',proxyURL+'/getEventRanges',data)
import cgi
print cgi.parse_qs(res.data)

# update event range
data = {'eventRangeID':'0-'+str(pandaID)+'-1-2-3-4',
        'secretKey':secretKey,
        'eventStatus':'finished',
        'baseURL':'https://aipanda007.cern.ch:25443/server/panda'}
res = http.request('POST',proxyURL+'/updateEventRange',data)
print res.data

# get key-pair
proxyURL = os.environ['PANDA_URL']
data = {'pandaID':pandaID,
        'publicKeyName':'BNL_ObjectStoreKey.pub',
        'privateKeyName':'BNL_ObjectStoreKey',
        'secretKey':secretKey,
        'baseURL':'https://aipanda007.cern.ch:25443/server/panda'}
res = http.request('POST',proxyURL+'/getKeyPair',data)
import cgi
print cgi.parse_qs(res.data)
