from django import template
from testik.models import Category, Question

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.filter(parent_id=None)


@register.simple_tag()
def get_child_categories(category_id):
    return Category.objects.filter(parent_id=category_id)


@register.simple_tag()
def get_num_plus(num):
    return int(num) +1
