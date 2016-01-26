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
def checkKeyWords(kwd,https=False):
    if not https:
        if not 'secretKey' in kwd:
            return False,None,None,'no secretKey'
        secretKey = kwd['secretKey']
        del kwd['secretKey']
    else:
        # dummy secret key for https
        secretKey = None
    if 'baseURL' in kwd:
        baseURL = kwd['baseURL'] 
        del kwd['baseURL']
        return True,secretKey,baseURL,kwd
    elif 'url' in kwd:
        url = kwd['url']
        del kwd['url']
        return True,secretKey,url,kwd
    else:
        return False,None,'no URL or baseURL'
    



# check permission
def hasPermission(req):
    # check hosts
    # TOBEDONE
    # host = req.get_remote_host()
    # check SSL
    if not req.subprocess_env.has_key('SSL_CLIENT_S_DN'):
        return False
    # check DN or role
    # FIXME to read from cfg
    if not '/DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=pandasv1/CN=531497/CN=Robot' in \
            req.subprocess_env['SSL_CLIENT_S_DN'] and \
            not '/DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=pandasv2/CN=614260/CN=Robot' in \
            req.subprocess_env['SSL_CLIENT_S_DN']:
        return False
    return True
