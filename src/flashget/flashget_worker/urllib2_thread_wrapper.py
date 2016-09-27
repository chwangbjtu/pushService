import threading
import urllib2

_url_opener = threading.local()

def get_opener():
    if hasattr(_url_opener,"opener"):
        return _url_opener.opener
    else:
        opener = urllib2.build_opener() 
        setattr(_url_opener,"opener",opener)
    return _url_opener.opener
