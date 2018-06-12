# coding=utf-8
from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def absolute_reverse(request, name):
    return request.build_absolute_uri(reverse(name))
