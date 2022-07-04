from django.shortcuts import render
from django.http import HttpResponse
from .models import TestResult


def main_page(request):
    return HttpResponse('Добро пожаловать на главную страницу')


def tests_page(request):
    return HttpResponse('Тут все тесты')


def description_test(request):
    return HttpResponse('Это описание к тесту')


def passing_test(request):
    return HttpResponse('Пользователь делает тест')


def result(request):
    return HttpResponse('Твой результат')


def history(request):
    results = TestResult.objects.filter(user_id=request.user.id)
    context = {"title": "История пройденных тестов", "results": results}
    return render(request, "testik/history.html", context)
