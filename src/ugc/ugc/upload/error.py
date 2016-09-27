#!/usr/bin/python
# -*- coding:utf-8 -*-

UPLOAD_ERROR_SUCCESS = 0
UPLOAD_ERROR_SERVER_EXCEPTION = 1
UPLOAD_ERROR_INVALID_FORM = 2
UPLOAD_ERROR_TOO_LARGE_FILE = 3
UPLOAD_ERROR_ILLEGAL_ACCESS = 4
UPLOAD_ERROR_FILE_EXPIRED = 5
UPLOAD_ERROR_AUTHENTICATION = 6
UPLOAD_ERROR_PERMISSION = 7

def pack_error(err_code):
    return '{"result":"fail","err":"%s"}' % parse_to_msg(err_code)

msg_list = ("ok","服务器异常,稍后重试","表单无效","文件超过最大限制","非法访问",
            "文件已过期,请重新上传","登录过期，请重新登录","您无权限进行此操作，请联系管理员")

def parse_to_msg(err_code):
    if not err_code < len(msg_list) or err_code < 0:
        return None
    return msg_list[err_code]


if __name__ == "__main__":
    for i in range(-3,10):
        code = i
        print code,"::",parse_to_msg(code)
    raw_input("press")