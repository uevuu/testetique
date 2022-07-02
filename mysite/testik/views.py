from django.shortcuts import render
from django.http import HttpResponse
from .models import Test, Category


def main_page(request):
    return HttpResponse('Добро пожаловать на главную страницу')


def tests_page(request):
    all_tests = Test.objects.all()
    categories = Category.objects.all()
    context = {
        'all_tests': all_tests,
        'categories': categories,
        'title': 'Наши тесты'
    }
    return render(request, template_name='testik/tests_page.html', context=context)


def get_category(request, category_id):
    all_tests = Test.objects.filter(category_id=category_id)
    categories = Category.objects.all()
    curr_category = Category.objects.get(pk=category_id)
    context = {
        'all_tests': all_tests,
        'categories': categories,
        'category': curr_category
    }
    return render(request, template_name='testik/category.html', context=context)


def description_test(request):
    return HttpResponse('Это описание к тесту')


def passing_test(request):
    return HttpResponse('Пользователь делает тест')


def result(request):
    return HttpResponse('Твой результат')


def history(request):
    return HttpResponse('История прохождения тестов')
