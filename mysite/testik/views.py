from django.shortcuts import render
from django.http import HttpResponse


def main_page(request):
    return HttpResponse('Тут все тесты')


def description_test(request):
    return HttpResponse('Это описание к тесту')


def passing_test(request):
    return HttpResponse('Пользователь делает тест')


def result(request):
    return HttpResponse('Твой результат')


def history(request):
    return HttpResponse('История прохождения тестов')
