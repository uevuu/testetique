from django.shortcuts import render
from django.http import HttpResponse
from .models import Test


def main_page(request):
    return HttpResponse('Добро пожаловать на главную страницу')


def tests_page(request):
    all_tests = Test.objects.all()
    return render(request, 'testik/tests_page.html', {'all_tests': all_tests, 'title': 'наши тесты'})
    # return HttpResponse('Тут все тесты')


def description_test(request):
    return HttpResponse('Это описание к тесту')


def passing_test(request):
    return HttpResponse('Пользователь делает тест')


def result(request):
    return HttpResponse('Твой результат')


def history(request):
    return HttpResponse('История прохождения тестов')
