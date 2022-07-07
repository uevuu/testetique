from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from .models import Test, Category, Question


def main_page(request):
    return HttpResponse('Добро пожаловать на главную страницу')


def tests_page(request):
    all_tests = Test.objects.all().order_by("-created_date")
    context = {
        'all_tests': all_tests,
        'title': 'Наши тесты'
    }
    return render(request, template_name='testik/tests_page.html', context=context)


def get_category(request, category_id):
    child_category = Category.objects.filter(parent_id=category_id)
    all_tests = Test.objects.filter(Q(category_id__in=child_category) | Q(category_id=category_id))
    curr_category = Category.objects.get(pk=category_id)
    context = {
        'all_tests': all_tests,
        'category': curr_category
    }
    return render(request, template_name='testik/category.html', context=context)


def description_test(request, test_id):
    curr_test = get_object_or_404(Test, pk=test_id)
    questions = Question.objects.filter(test_id=test_id)
    context = {
        'test': curr_test,
        'questions': questions
    }
    return render(request, template_name='testik/test.html', context=context)


def filter_tests(request):
    if request.GET:
        child_list = request.GET.getlist("category")
        sort_param = request.GET.getlist("sort_param")[0]
        child_category = Category.objects.filter(parent_id__in=child_list)
        category_list = request.GET.getlist("category")
        child_list = [int(_) for _ in child_list]
        if len(child_list) == 0:
            tests = Test.objects.all().order_by(sort_param)
        else:
            tests = Test.objects.filter(
                Q(category_id__in=category_list) | Q(category_id__in=child_category)).order_by(sort_param)
        context = {
            'all_tests': tests,
            'child_list': child_list,
            'sort_param': sort_param,
        }
        return render(request, template_name='testik/tests_page.html', context=context)
    return tests_page(request)


# def index(request):
#     user_search = request.GET.get('search')
#     tests = Test.objects.filter(Q(description__icontains=user_search) | Q(title__icontains=user_search))
#     context = {'all_tests': tests}
#     return render(request, template_name='testik/tests_page.html', context=context)


def sort_tests(request):
    pass


def passing_test(request):
    return HttpResponse('Пользователь делает тест')


def result(request):
    return HttpResponse('Твой результат')


def history(request):
    return HttpResponse('История прохождения тестов')
