#!/usr/bin/python
# -*- coding:utf-8 -*-

def is_bad_sql_string(str_arg):
    if not str_arg:
        return False
    if "\"" in str_arg or "'" in str_arg:
        return True
    return False


def exist_bad_sql_string(*args):
    for item in args:
        if is_bad_sql_string(item):
            return True
    return False


def sql_build_set_value(pair_list):
	sql_sentence = ""
	for seg in pair_list:
		if not seg[1]:
			continue
		if sql_sentence:
			sql_sentence += ","
		if isinstance(seg[0],str) or isinstance(seg[0],unicode):
			sql_sentence += "%s='%s'" % (seg[0],str(seg[1]))
		else:
			sql_sentence += "%s=%s" % (seg[0],str(seg[1]))
	return sql_sentence


def  _output_list(in_list):
     ret_list = []
     try:
         for item in in_list:
             str_temp = "'%s'" % (item)                
             ret_list.append(str_temp)
         return ret_list
     except Exception,e:
         return ret_list

def sql_build_value(input_list):
        sql_sentence = ""
        value_list = _output_list(input_list)
        if len(value_list) == 0:
            return  sql_sentence
        for seg in value_list:
            if sql_sentence:
                sql_sentence += ","
            if isinstance(seg,str) or isinstance(seg,unicode):
                sql_sentence += "%s" % (seg)
            else:
                sql_sentence += "%s" % (seg)
        sql_sentence = "(%s)" % sql_sentence
        return sql_sentence





