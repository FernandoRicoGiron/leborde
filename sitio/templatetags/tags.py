import itertools
from django import template
register = template.Library()

@register.filter
def replace(value):
    return value.replace(" ","").replace("/","")

@register.filter
def replace2(value, re):
    remplazo = value.replace(re,"")
    return remplazo