from django import template
register = template.Library()

@register.filter(name='access')
def access(dic, key):
    if key in dic:
        return dic[key]
