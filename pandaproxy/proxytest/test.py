# $ source /data/atlpan/srv/etc/sysconfig/panda_proxy-sysconfig
# $ python /data/atlpan/srv/lib/python*/site-packages/pandaproxy/proxytest/test.py

import os
import uuid
import requests

# key registeration : used by only the panda server
ca_certs='/etc/pki/tls/certs/CERN-bundle.pem'
key_file=os.environ['X509_USER_PROXY']
cert_file=os.environ['X509_USER_PROXY']

pandaID = 123
proxyURLSSL = 'https://aipanda084.cern.ch:25128/proxy/panda'
data = {'pandaID':pandaID}
res = requests.post(proxyURLSSL+'/insertSecretKeyForPandaID',
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

# dummy jobsetID just for test
jobsetID = 567

# get event ranges 
proxyURL = 'http://aipanda084.cern.ch:25064/proxy/panda'
data = {'pandaID':pandaID,
        'jobsetID':jobsetID,
        'secretKey':secretKey,
        'baseURL':'https://pandaserver.cern.ch:25443/server/panda'}
res = requests.post(proxyURL+'/getEventRanges',data)
import cgi
print cgi.parse_qs(res.text.encode('ascii'))


# dummy evetRangeID just for test
eventRangeID = '0-'+str(pandaID)+'-1-2-3-4'

# update event range
data = {'eventRangeID':eventRangeID,
        'secretKey':secretKey,
        'eventStatus':'finished',
        'baseURL':'https://pandaserver.cern.ch:25443/server/panda'}
res = requests.post(proxyURL+'/updateEventRange',data)
print res.text.encode('ascii')

# get key-pair
data = {'pandaID':pandaID,
        'publicKeyName':'BNL_ObjectStoreKey.pub',
        'privateKeyName':'BNL_ObjectStoreKey',
        'secretKey':secretKey,
        'baseURL':'https://pandaserver.cern.ch:25443/server/panda'}
res = requests.post(proxyURL+'/getKeyPair',data)
tmpDict = cgi.parse_qs(res.text.encode('ascii'))
print tmpDict

privateKey = tmpDict['privateKey'][0]
publicKey  = tmpDict['publicKey'][0]


# upload file
fileName = uuid.uuid4().hex
data = {'pandaID':pandaID,
        'secretKey':secretKey,
        'publicKey':publicKey,
        'privateKey':privateKey,
        'url':'http://cephgw.usatlas.bnl.gov:8443/pandaproxytest2/'+fileName}
files = {'uploadFile':(fileName,open('favicon.ico','rb'))}
print data
res = requests.post(proxyURL+'/setFileToS3',data=data,files=files)
print res.text

# get file info
data = {'pandaID':pandaID,
        'secretKey':secretKey,
        'publicKey':publicKey,
        'privateKey':privateKey,
        'url':'http://cephgw.usatlas.bnl.gov:8443/pandaproxytest2/'+fileName}
res = requests.post(proxyURL+'/getFileInfo',data=data)
print cgi.parse_qs(res.text.encode('ascii'))

# download file
fH = open('{0}.out'.format(fileName),'wb')
data = {'pandaID':pandaID,
        'secretKey':secretKey,
        'publicKey':publicKey,
        'privateKey':privateKey,
        'url':'http://cephgw.usatlas.bnl.gov:8443/pandaproxytest2/'+fileName}
res = requests.post(proxyURL+'/getFileContent',data=data,stream=True)
for chunk in res.iter_content(chunk_size=1024): 
    if chunk:
        fH.write(chunk)
        fH.flush()
fH.close()
print res.status_code

