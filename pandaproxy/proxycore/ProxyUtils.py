# dummy request object
class DummyReq:
    # constructor
    def __init__(self,env,):
        # environ
        self.subprocess_env = env
        # header
        self.headers_in = {}
        # content-length
        if self.subprocess_env.has_key('CONTENT_LENGTH'):
            self.headers_in["content-length"] = self.subprocess_env['CONTENT_LENGTH']

    # get remote host    
    def get_remote_host(self):
        if self.subprocess_env.has_key('REMOTE_HOST'):
            return self.subprocess_env['REMOTE_HOST']
        return ""



# check key words
def checkKeyWords(kwd,https=False,isBulk=False):
    if not https:
        if not 'secretKey' in kwd:
            return False,None,None,'no secretKey'
        secretKey = kwd['secretKey']
        del kwd['secretKey']
    else:
        # dummy secret key for https
        secretKey = None
    if isBulk:
        return True,secretKey,None,kwd
    elif 'baseURL' in kwd:
        baseURL = kwd['baseURL'] 
        del kwd['baseURL']
        return True,secretKey,baseURL,kwd
    elif 'url' in kwd:
        url = kwd['url']
        del kwd['url']
        return True,secretKey,url,kwd
    else:
        return False,None,'no URL or baseURL'
    

# get FQANs
def getFQANs(req):
    fqans = []
    for tmpKey,tmpVal in req.subprocess_env.iteritems():
        # compact credentials
        if tmpKey.startswith('GRST_CRED_'):
            # VOMS attribute
            if tmpVal.startswith('VOMS'):
                # FQAN
                fqan = tmpVal.split()[-1]
                # append
                fqans.append(fqan)
        # old style         
        elif tmpKey.startswith('GRST_CONN_'):
            tmpItems = tmpVal.split(':')
            # FQAN
            if len(tmpItems)==2 and tmpItems[0]=='fqan':
                fqans.append(tmpItems[-1])
    # return
    return fqans



# check permission
def hasPermission(req):
    # check hosts
    # TOBEDONE
    # host = req.get_remote_host()
    # check SSL
    if not req.subprocess_env.has_key('SSL_CLIENT_S_DN'):
        return False
    # check role
    fqans = getFQANs(req)
    for fqan in fqans:
        for rolePat in ['/atlas/Role=production']:
            if fqan.startswith(rolePat):
                return True
    return False
