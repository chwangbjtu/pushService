# -*-coding:utf-8 -*-
import urllib 
import urllib2
import json

def get(url):
    response = urllib2.urlopen(url)
    content = response.read()
    return content

def post(url, data):
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    content = response.read()
    return content
    
def test_regist_new():
    device_info = {}
    device_info['token'] = '42b431506eb2fb6410b2337254ae40eee63e498f527c5ba1499da049ce3bc2ca'
    device_info['mac'] = 'fdsfsdf::bd78:21a3:6953:93a5%18'
    device_info['app_name'] = "funshionTV"
    device_info['version'] = '1.0.1'
    device_info['os'] = 'ios9.2'
    device_info['hardware'] = 'XSDFSD_DSAEFCA_?dwdd'
    device_info['group'] = '123'
    device_info['channelid']=''
    device_info['platform']=''
    
    url = "http://icontent.push.funshion.com/v2/app/register"
    post_data = json.dumps(device_info)
    response = post(url, post_data)
    print response
    
def test_delete_tk():
    info = {}
    info['device_token'] = []
    info['device_token'].append('38db0bd8f2ff3e8274957d49b0ae21e5c74fd65a06cae0d2d10b0a0ff2caaf5f')
    
    url = "http://127.0.0.1:19000/v2/service/del_token"
    post_data = json.dumps(info)
    
    response = post(url, post_data)
    print response
    
def test_regist_v1():    
    url_params = {}
    url_params['deviceid'] = 'fdsfsdf::bd78:21a3:6953:93a5%18'
    url_params['devicetoken'] = '<e6555d5f a640079c 0450a5f5 1c862440 5da80d21 2e86ddc7 a740f54d a9420b44>'
    url_params['os_type'] = "funshionTV"
    url_params['sys_ver'] = 'ios9.2'
    url_params['hardware_info'] = 'XSDFSD_DSAEFCA_?dwdd'
    url_params['cli_ver'] = '1.0.1'
    
    str_params = urllib.urlencode(url_params)
    url = "http://127.0.0.1:8000/api/regist.php?" + str_params
    
    response = get(url)
    print response
    
def test_regist_v2():
    url_params = {}
    url_params['mac'] = 'fdsfsdf::bd78:21a3:6953:93a5%18'
    url_params['token'] = 'e6555d5fa640079c0450a5f51c8624405da80d212e86ddc7a740f54da9420b44'
    url_params['app_name'] = "funshionTV"
    url_params['os'] = 'ios9.2'
    url_params['hardware'] = 'XSDFSD_DSAEFCA_?dwdd'
    url_params['version'] = '1.0.1'
    url_params['group'] = '123'
    
    str_params = urllib.urlencode(url_params)
    url = "http://127.0.0.1:8000/v2/push/regist?" + str_params
    
    response = get(url)
    print response
    
if __name__ == '__main__':
    test_regist_new()
    #test_delete_tk()
    #test_regist_v1()
    #test_regist_v2()
    
