#-*- coding: utf-8 -*-
import sys
import getopt
sys.path.append("../")
from apnslib.notification import *
from apnslib.notify_mgr import *

def Usage():
    print "apns测试脚本，用法:"
    print "-t 推送给指定token的设备"
    print "-m 推送的消息"
    print "-a 推送给哪个app,iphone,ipad,funshionTV,ipadplayerplus"
    print "示例：python test_apns.py -m lalala -t 38db0bd8f2ff3e8274957d49b0ae21e5c74fd65a06cae0d2d10b0a0ff2caaf5f -a funshionTV"
    
def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'ha:m:t:')
        app = None
        msg = None
        token = None
        
        for op, var in opts:
            if op == '-a':
                app = var
                
            elif op == '-m':
                msg = var
                
            elif op == '-t':
                token = var
                
            else:
                Usage()
            
        if not token or not msg or not app:
            raise Exception("参数错误")
            
        obj = APNSNotificationWrapper(app, False)
        message = APNSNotification()
        message.token_hex(token)
        message.badge(1)
        
        alert_l = APNSAlert()
        alert_l.set_body(msg)
        message.alert(alert_l)
        
        obj.append(message)
        obj.notify()
    
    except Exception, e:
        print str(e)
        Usage()
        
if __name__ == "__main__":
    main(sys.argv)