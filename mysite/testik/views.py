from django.shortcuts import render
from django.http import HttpResponse
from .models import TestResult, Test, Category, Question


def main_page(request):
    return HttpResponse('Добро пожаловать на главную страницу')


def tests_page(request):
    all_tests = Test.objects.all()
    context = {
        'all_tests': all_tests,
        'title': 'Наши тесты'
    }
    return render(request, template_name='testik/tests_page.html', context=context)


def get_category(request, category_id):
    all_tests = Test.objects.filter(category_id=category_id)
    curr_category = Category.objects.get(pk=category_id)
    context = {
        'all_tests': all_tests,
        'category': curr_category
    }
    return render(request, template_name='testik/category.html', context=context)


def description_test(request, test_id):
    curr_test = Test.objects.get(pk=test_id)
    questions = Question.objects.filter(test_id=test_id)
    context = {
        'test': curr_test,
        'questions': questions
    }
    return render(request, template_name='testik/test.html', context=context)


def passing_test(request):
    return HttpResponse('Пользователь делает тест')


def result(request):
    return HttpResponse('Твой результат')


def history(request):
    results = TestResult.objects.filter(user_id=request.user.id)
    context = {"title": "История пройденных тестов", "results": results}
    return render(request, "testik/history.html", context)
