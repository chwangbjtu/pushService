#!/usr/bin/python
# -*- coding:utf-8 -*-
#在此定义一些公用方法，可以在django模板中使用set、import、print
from django import template  
import re  
register = template.Library()  
  
set_regex = re.compile(r'^\s*set\s+(\w+)\s*=\s*(.*)$')  
def do_set(parser, token):  
    m = re.match(set_regex, token.contents)  
    if m:  
        name, exp = m.group(1), m.group(2)  
        return SetNode(name, exp)  
    else:  
        raise template.TemplateSyntaxError('{% set varname = python_expression %}')  
      
class SetNode(template.Node):  
    def __init__(self, varname, expression):  
        self.varname = varname  
        self.expression = expression  
  
    def render(self, context):  
        context[self.varname] = eval(self.expression, {}, context)  
        return ''  
  
register.tag('set', do_set)      
  
  
print_regex = re.compile(r'^\s*print\s+(.*)$')  
def do_print(parser, token):  
    m = re.match(print_regex, token.contents)  
    if m:  
        exp = m.group(1)  
        return PrintNode(exp)  
    else:  
        raise template.TemplateSyntaxError('{% print expression %}')  
  
class PrintNode(template.Node):  
    def __init__(self, expression):  
        self.expression = expression  
  
    def render(self, context):  
        obj = eval(self.expression, {}, context)  
        return str(obj)  
  
register.tag('print', do_print)  
  
  
import_regex = re.compile(r'^\s*import\s+(\S+)(?:\s+as\s+(\w+))?$')  
def do_import(parser, token):  
    m = re.match(import_regex, token.contents)  
    if m:  
        exp = m.group(1)  
        try:  
            alias = m.group(2)  
        except:  
            alias = None  
        return ImportNode(exp, alias)  
    else:  
        raise template.TemplateSyntaxError('{% import import_expression [ as alias_name ] %}')  

class ImportNode(template.Node):  
    def __init__(self, expression, alias=None):  
        if not alias: alias = expression  
        self.expression = expression  
        self.alias = alias  
  
    def render(self, context):  
        module = __import__(self.expression, {}, context)  
        context[self.alias] = module  
        return ''  
  
register.tag('import', do_import) 


@register.filter(name='getkey')
def getkey(value, arg):
    return value[arg]

@register.filter(name='join')
def join(value):
    return ",".join(value)
