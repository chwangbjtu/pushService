"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import audit_mgr
import constant
import json
import time
from audit_modify_info import AuditModifyInfo
from audit_modify_info import ApplyTaskInfo

def test_apply_task(audit):
    uid = 4
    task_count = 2  #task count
    
    #申请任务
    print '1 test_apply_task---begin---'
    (code,res) = audit.apply_task(uid, task_count)
    if code == constant.SUCCESS:
        print 'haha , %d apply_task  %s tasks ok.' % (uid, res)
        #print res, type(res)
    else:
        print 'not success.', code, res

    print '1 test_apply_task---end---'



def test_apply_task_v2(audit):
   
    #task_count = 2  #task count
    uid = 4
    apply_num = 2
    site = 'yk'
    channel = ''
    title = ''
    fname = 'spider'
    #title = ''
    apply_info =  ApplyTaskInfo(uid, apply_num, site, channel, title,fname)

    #申请任务
    print '1 test_apply_task_v2---begin---'
    (code,res) = audit.apply_task(apply_info)
    if code == constant.SUCCESS:
        print 'haha , %d apply_task_v2  %s tasks ok.' % (uid, res)
        #print res, type(res)
    else:
        print 'not success.', code, res

    print '1 apply_task_v2---end---'



def create_duration(duration):
        try:
            import time
            createValue = duration
            createValue = float(createValue)
            createValue /= 1000
            return time.strftime('%H:%M:%S', time.gmtime(createValue))
        except Exception, e:
            return None
#for client test.
if __name__ == "__main__":
    uid = 4   #user id
    
    audit = audit_mgr.AuditMgr.instance()
    #test_apply_task(audit, uid)
    #test_apply_task_v2(audit)
    list = ()
    print len(list)


    '''
    begin_time = '2013-06-21'
    end_time = '2013-06-30'
    page = 1
    page_size = 10
    (code, res1, res2) = audit.get_dat_macros_statics_list(begin_time, end_time, page_size, page)
    print code, res1, res2
    '''

    '''
    page = 1
    page_size = 10
    #key_search = 'C61D3FCDFA605EF6C6F45A3398EF6A3B0AF667C9'
    #key_type = "dat"

    key_search = 'e2a0b21a72f29112282279f97a31fe4aca1eadce'
    key_type = "funshion"
    ret = audit.search_mp4_info_from_dat(key_search, key_type , page_size, page)
    print ret[0], ret[1], ret[2]
    '''


    '''
    page = 1
    pagesize = 30

    test_map = {}
    test_map['1'] = "sdfsfsfsf"
    if  test_map.has_key('1'):
        print 'has key 1.'
    else:
        test_map['1'] = "liu"
       
    test_map['2'] = "zhousdfkslfs"
    test_map['3'] = "tttttt"
    for item in test_map:
        print item , test_map[item]

    from collections import Counter
    a=['a','b','c','d','a','d','a','c']
    print Counter(a)

    btime = '2013-05-20'
    etime = '2013-05-22'
    (code, res) = audit.get_audit_statics_info(btime, etime, -1, page)
    print code, res

    time = '2013-05-20'
    (code, res) = audit.get_audit_statics_info(btime, etime, pagesize, page)
    print code, res

    duration = 108400
    ret = create_duration(duration)
    print 'time: ', ret
    '''

    '''
    (code, res) = audit.get_forwards_userspace(uid, -1, page)
    print code, res
    if code != constant.SUCCESS:
        print '(7) get number  error.'
    else:
        print '(6) get number'
        print res


    (code, res) = audit.get_forwards_userspace(uid, pagesize, page)
    print code, res
    if code != constant.SUCCESS:
        print '(7) get_forwards_userspace error.'
    else:
        print '(6) get_forwards_userspace'
        print res
    '''


    #----获取所有视频信息和获取待审核的接口就是一个get_pending_tasklist，获取所有视频信息uid=None

    '''
    #获取待审核任务列表
    #(1) 取记录数
    (code, res) = audit.get_pending_tasklist(uid, -1, page)  #get the record 
    print code, res
    if code == constant.SUCCESS:
        print '(2-1) haha , get total number ok.'
        print 'number: ', res
    else:
        print '(2-1) get total number  error.'

    print '----------get tasklist- begin--'

    #(2) 获取分页信息
    (code, res) = audit.get_pending_tasklist(uid, pagesize, page)  #get the record 
    print code, res
    if code == constant.SUCCESS:
        print '(2-2) haha , get_pending_tasklist ok.'
        print res
        for item in res:
            ret_json = json.loads(item)
            print ret_json['uid'], ret_json['tid'], ret_json['title']
    else:
        print '(2-2) get_pending_tasklist error.'
    '''
    
    '''
    #获取所有视频任务列表, 能够获取总记录数和所有视频的分页信息, 接口同上待审核
    uid = 4   #get the 
    (code, res) = audit.get_all_tasklist(uid, -1, page)  #get the all record number
    #print code, res
    if code == constant.SUCCESS:
        print '(3-1)*** get all tasklist number:', res
    else:
        print 'get all tasklist  error.'

    (code, res) = audit.get_all_tasklist(uid, pagesize, page)  #get the record
    #print code, res
    if code == constant.SUCCESS:
        print '(3-2)***  get all tasklist ok.'
        print res
        for item in res:
            ret_json = json.loads(item)
            print ret_json['uid'], ret_json['tid'], ret_json['title']
    else:
        print '(3-2) get all tasklist error.'
    '''
    
    #time.sleep(1)
    '''
    #获取已审核任务列表
    uid = 1
    (code, res) = audit.get_passed_tasklist(uid, -1, page)  #get the all record number
    #print code, res
    if code == constant.SUCCESS:
        print '(4-1)*** get_passed_tasklist number:', res
    else:
        print 'get all tasklist  error.'

    (code, res) = audit.get_passed_tasklist(uid, pagesize, page)  #get the record 1 and 3
    if code == constant.SUCCESS:
        print '(4-2) haha , get_passed_tasklist ok.'
        print res
        for item in res:
            ret_json = json.loads(item)
            print ret_json['uid'], ret_json['tid'], ret_json['title']
    else:
        print '(4-2) get_passed_tasklist error.'

    
    #获取审核失败任务列表
    (code, res) = audit.get_failure_tasklist(uid, -1, page)  #get the all record number
    #print code, res
    if code == constant.SUCCESS:
        print '(5-1)*** get_failure_tasklist number:', res
    else:
        print 'get all tasklist  error.'
    (code, res) = audit.get_failure_tasklist(uid, pagesize, page)  #get the record 1 and 3
    if code == constant.SUCCESS:
        print '(5-2) haha , get_failure_tasklist ok.'
        print res
        for item in res:
            ret_json = json.loads(item)
            print ret_json['uid'], ret_json['tid'], ret_json['title']
    else:
        print '(5-2) error in get_failure_tasklist'


    print '--------get tasklist--end--'
    '''

    '''
    #退订审核任务
    tidlist = []
    tidlist.append('555')   #存放tid
    tidlist.append('334')
    (code, res) = audit.cancel_task(uid, tidlist)  #get the record 1 and 3
    if code == constant.SUCCESS:
        print '(5) haha , cancel_task ok.'
        print res
    else:
        print 'cancel_task error.'
    

    
    #审核视频
    uid = 1
    tid = '151368432030.15'
    funshion_id =  'd2a956cdeefdf050545ec67bd53cba3b2a29e531'
    result = 1
    #(code, res) = audit.audit_video(uid, tid, result)
    modify_info = AuditModifyInfo()   #修改的审核数据信息结构体
    #modify_info.title = "测试开发"
    #modify_info.channel = "sdfsfsfsfs"
    #modify_info.funshion_id =  'ABCDFASDF111'
    modify_info.logo = "http://ugcimg.funshion.com:8089/2013_04_03/6d0eaa4b616142c9bcec614448edb7bcb06df2e6.jpg"
    (code, res) = audit.audit_video(uid, tid, funshion_id, result, modify_info)  
    if code == constant.SUCCESS:
        print '(5) haha , audit_video ok.'
        print res
    else:
        print 'audit_video error.'
    
    #由tid获取详细信息，转码后的信息
    #uid = 1
    tid = '222'
    (code, res) = audit.get_audit_task_details(tid)
    print code, res
    if code != constant.SUCCESS:
        print '(6) haha, get the audit_task_details error.'
    else:
        print '(6) get task details ok.'
        print res
        for item in res:
            info = json.loads(item)
            print info['uid'], info['tags'], info['title'],info['funshion_id']
        #print info
        print 'byebye'

    #由tid获取基本数据信息
    tid = '334'
    (code, res) = audit.get_video_base(tid)
    print code, res
    if code != constant.SUCCESS:
        print '(7) haha, get db_get_video_base error.'
    else:
        print '(7) db_get_video_base ok.'
     #  print res
        info = json.loads(res)
        print info['uid'], info['username'], info['tags'], info['title'], info['video_id']
    '''

    audit.close()
    