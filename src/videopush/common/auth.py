
class Auth(object):

    def __init__(self):
        pass

    def auth_key(self, site, key):
        if site not in ['brave', 'xhgj', 'kkn']: 
            return False
        return True
