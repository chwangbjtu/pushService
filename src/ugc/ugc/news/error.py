#!/usr/bin/python
# -*- coding:utf-8 -*-  

import json

#protocal exception
ERROR_HTTP_URL_NOT_SUPPORTED = ("00.00","url not supported")
ERROR_HTTP_METHOD_NOT_SUPPORTED = ("00.01","http method not supported")

#businiess base protocal exception
ERROR_JSON_SYNTAX_ERROR = ("01.00","syntax error to json")

#business logic error
ERROR_PARAM_NO_PRIMARY_KEY = ("02.00","primary key missing")
ERROR_PARAM_INVALID_VALUE = ("02.01","invalid value to key")
ERROR_PARAM_NO_KEY      =   ("02.02","no such key")
ERROR_PARAM_ARG_MISSING = ("02.03","parameter missing")

ERROR_PARAM_INVALID_PARAMETER = ("10.00","invalid parameter parameter")
ERROR_PARAM_INVALID_KEY      =   ("10.02","invalid field")
ERROR_PARAM_KEY_ALREADY_EXISTS = ("10.03","specified key already exists")
ERROR_PARAM_KEY_NOT_EXIST      = ("10.04","specified key not exists")

ERROR_SYSTEM_DATABASE = ("20.00","database throwed exception")
ERROR_SYSTEM_NOT_AUTHENTICATED = ("20.01","not authenticated")

ERROR_INTERNAL_SERVER_ERROR = ("90.00","server internal error")

def pack_errinfo_json(error,detail=None):
    result = {"result":"fail","err":{}}
    result["err"]["code"] = error[0]
    result["err"]["info"] = error[1]
    if detail:
        result["err"]["parameter"] = detail
    result = json.dumps(result)
    return result


if __name__ == "__main__":
    print pack_errinfo_json(ERROR_INTERNAL_SERVER_ERROR,"shit")
    raw_input()