import httplib, urllib
import json
import time

if __name__ == "__main__":
    content = {"origin": "upload", "audit_free": "no", "describe": "1414", "uid": 1, "vid": "http://192.168.16.118:8000/upload/download/?filename=tmp5nNIlB.upload", "title": "14124", "tags": "14141", "site": "cntv", "priority": 7, "channel":u"\u65B0\u95FB"}
    remote  = "127.0.0.1:6808"
    path    = "/maze/addtask"
    headers = {"X-Forwarded-For":"192.168.1.1", "Content-type": "application/x-www-form-urlencoded","Accept": "text/plain,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
    total = 0
    error_number = 0
    begin = time.time()
    while True:
        try:
            total = total + 1
            conn = httplib.HTTPConnection(remote)
            conn.request("POST", path, json.dumps(content), headers)
            resp = conn.getresponse()
            body = resp.read() 
            #print resp.status, body
            ret = json.loads(body)
            if ret["result"] != "ok":
               error_number = error_number + 1
            print total, error_number
            if total >= 10000:
               break 
        except Exception, err:
            print err
            error_number = error_number + 1
    end = time.time()
    print "total: ", total, "time: ", end-begin, "rps:", total/(end-begin)
            
                
