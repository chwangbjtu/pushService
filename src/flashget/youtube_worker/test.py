#!/usr/bin/python
# -*- coding:utf-8 -*-  

import time
import sys
import os
import signal
import subprocess     

if __name__ == "__main__":
    try:
    
        #t_f = os.popen ("scp -i ./key/id_rsa -P 5044 ./pypost.py crawler@111.161.35.219:/tmp/")
        #print t_f.read()

        str1 = "/usr/bin/rsync -avzP --password-file=/tmp/rt/rsync.passwd " + "/tmp/youtube-dl" + " spider@111.161.35.219::ugc/"
        start = int(time.time())
        p = subprocess.Popen(str1,shell=True)
        if True:
            res = None
            res =  p.poll()
            time.sleep(1)

            now = int(time.time())
            if now - start > 60:
                os.kill(p.pid, signal.SIGKILL)
                os.waitpid(-1, os.WNOHANG)
                print "return 1"

            print "returncode",p.returncode

            if res is None:
                print "res is NOne"
                pass
            else:
                print "res",res
                p.wait()
                #break

    except Exception, err:
        print "err", err
