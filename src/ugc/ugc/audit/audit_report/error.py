#!/usr/bin/python
# -*- coding:utf-8 -*-

#protocal exception
ERROR_HTTP_URL_NOT_SUPPORTED = ("00.00", "url not supported")
ERROR_HTTP_METHOD_NOT_SUPPORTED = ("00.01", "http method not supported")

#businiess base protocal exception
ERROR_JSON_SYNTAX_ERROR = ("01.00", "syntax error to json")

#business logic error
ERROR_URL_DOMAIN = ("02.00", "url domain is invalid.")

ERROR_START_URL = ("02.10", "url start error.")

ERROR_PARAM_URL = ("02.10", "parameter error.")

ERROR_URL_GETTUDOU = ("02.00", "tudou url get html error.")

ERROR_URL_PARSER = ("02.00", "vid parse error.")

STATUS_ADD_ERROR = ("02.56", "task status operate error in server.")

STATUS_ADD_FORBIDDEN = ("02.05", "forbidden, the tid is invalid.")

EXCEPTION_CLOSE = ("02.01", "exception close.")

EXCEPTION_GET_URL = ("02.50", "has exception to get url.")
ERROR_PARAM_ARG_MISSING = ("02.03", "parameter missing")

def pack_errinfo_json(error):
    result = '{"result":"fail", "errcode":"%s", "err":"%s"}' % error
    return result
