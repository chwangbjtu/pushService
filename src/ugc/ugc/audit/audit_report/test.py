import verify_data_mgr
import verify_infohash_mgr
import verify_ms_info_mgr
import json
import constant

def verify_data():
     verify_str = "{\"info\": [{\"video_url\": \"http://192.168.16.35:8089/bbbb__cccc/fa957225107cc74bdcd6b992f60e970b6551a7b8_biaoqing_1618957_23080.mp4\", \"filename\": \"fa957225107cc74bdcd6b992f60e970b6551a7b8.mp4\",\"rate\": \"biaoqing\",\"funshion_id\": \"fa957225107cc74bdcd6b992f60e970b6551a7b8\",\"img_url\": [\"http://ugcimg.funshion.com:8089/2013_05_10/fa957225107cc74bdcd6b992f60e970b6551a7b8_1.jpg\", \"http://ugcimg.funshion.com:8089/2013_05_10/fa957225107cc74bdcd6b992f60e970b6551a7b8_6.jpg\",\"http://ugcimg.funshion.com:8089/2013_05_10/fa957225107cc74bdcd6b992f60e970b6551a7b8_2.jpg\",\"http://ugcimg.funshion.com:8089/2013_05_10/fa957225107cc74bdcd6b992f60e970b6551a7b8_4.jpg\", \"http://ugcimg.funshion.com:8089/2013_05_10/fa957225107cc74bdcd6b992f60e970b6551a7b8_5.jpg\",\"http://ugcimg.funshion.com:8089/2013_05_10/fa957225107cc74bdcd6b992f60e970b6551a7b8.jpg\",\"http://ugcimg.funshion.com:8089/2013_05_10/fa957225107cc74bdcd6b992f60e970b6551a7b8_3.jpg\"],\"milliseconds\": \"23080\", \"size\": \"1618957\"}],\"ip\": \"192.168.16.35\", \"state\": \"success\", \"port\": \"8100\", \"tid\": \"bbbb__cccc\"}"
     try:
         data_json =  json.loads(verify_str)
         
         verify_data = verify_data_mgr.VerifyDataMgr().instance()
         print 'tid: ', data_json['tid']
         print type(verify_str), verify_str
         #print 
         (code, res) = verify_data.process(data_json)
         if code != constant.SUCCESS:
             print 'code: ', code, res
         print 'VerifyDataMgr::process ok .'
     except Exception,e:
         print e

def verify_infohash():
     infohash_str = "{\"infohash\":\"afa957225107cc74bdcd6b992f60e970b6551a7\", \"files\":[{\"funshion_id\":\"fa957225107cc74bdcd6b992f60e970b6551a7b8\", \"tid\":\"bbbb__cccc\"},{\"funshion_id\":\"fa957225107cc74bdcd6b992f60e970b6551a7b8\", \"tid\":\"bbbb__cccc\"}]}"
     try:
         data_json =  json.loads(infohash_str)
         
         verify_data = verify_infohash_mgr.VerifyInfohashMgr.instance()
         print 'infohash: ', data_json['infohash']
         print type(infohash_str), infohash_str
         #print 
         (code, res) = verify_data.process(data_json)
         if code != constant.SUCCESS:
             print 'code: ', code, res
         print 'verify_infohash::process ok .'
     except Exception,e:
         print e

def verify_mserver_info():
     mserver_info = "{\"infohash\":\"afa957225107cc74bdcd6b992f60e970b6551a7\", \"size\":123, \"server_ip\":\"192.168.135.23\", \"server_port\":\"8089\"}"
     try:
         data_json =  json.loads(mserver_info)
         
         verify_data = verify_ms_info_mgr.VerifyMsInfoMgr.instance()
         print 'infohash: ', data_json['infohash']
         print type(mserver_info), mserver_info
         #print 
         (code, res) = verify_data.process(data_json)
         if code != constant.SUCCESS:
             print 'code: ', code, res
         print 'verify_mserver_info::process ok .'
     except Exception,e:
         print e

if __name__ == '__main__':
     #verify_data()
     #verify_infohash()
     verify_mserver_info()
         

