########################################################################################
# REFERENCES
#  Title: Django documentation
#  Author: Django Software Foundation and individual contributors
#  Date: 2021
#  Date Cited: 5/03/2022
#  Code version: 4.0
#  URL: https://docs.djangoproject.com/en/4.0/howto/custom-template-tags/
#  Software License: BSD-3-Clause License
#
########################################################################################

from django import template

register = template.Library()

@register.filter(name='div')
def div(value, arg):
    """integer division"""
    if not value: return ''
    return int(value) // int(arg)

@register.filter(name='mod')
def mod(value, arg):
    """modulo operator"""
    if not value: return ''
    return int(value) % int(arg)
