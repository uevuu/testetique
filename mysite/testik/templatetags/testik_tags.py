from django import template
from testik.models import Category, Question

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_questions():
    return Question.objects.all()
