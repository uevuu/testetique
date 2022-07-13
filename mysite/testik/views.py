from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .forms import UserRegisterForm, UserLoginForm
from .models import TestResult, Test, Category, Question
from .services import processing_user_answers
from math import ceil
from datetime import datetime


def main_page(request):
    context = {}
    return render(request, 'testik/main_page.html', context)


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            return redirect("tests")
        else:
            messages.error(request, "Неудачная попытка регистрации")
    else:
        form = UserRegisterForm()
    content = {'form': form,
               'form_title': "Регистрация",
               "button_title": "Зарегистрироваться"}
    return render(request, 'testik/auth.html', content)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            return redirect('tests')
    else:
        form = UserLoginForm()
    content = {'form': form,
               'form_title': "Авторизация",
               "button_title": "Авторизоваться"}
    return render(request, 'testik/auth.html', content)


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def tests_page(request):
    all_tests = Test.objects.all().order_by("-created_date")
    context = {
        'all_tests': all_tests,
        'sort_param': '-created_date'
    }
    return render(request, 'testik/tests_page.html', context)


@login_required
def get_category(request, category_id):
    child_category = Category.objects.filter(parent_id=category_id)
    if len(request.GET.getlist("sort_param")) == 0:
        sort_param = "-created_date"
    else:
        sort_param = request.GET.getlist("sort_param")[0]
    all_tests = Test.objects.filter(Q(category_id__in=child_category) | Q(category_id=category_id)).order_by(sort_param)
    curr_category = Category.objects.get(pk=category_id)
    context = {
        'all_tests': all_tests,
        'category': curr_category,
        'sort_param': sort_param
    }
    return render(request, 'testik/category.html', context)


@login_required
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
        return render(request, 'testik/tests_page.html', context)
    return tests_page(request)


@login_required
def search_test(request):
    test_name = request.GET.get('test_title').replace('+', ' ')
    sort_param = request.GET.get("sort_param")
    if sort_param is None:
        sort_param = "-created_date"
    tests = Test.objects.filter(
        Q(title__contains=test_name.capitalize()) | Q(description__contains=test_name.capitalize()) |
        Q(title__contains=test_name.lower()) | Q(description__contains=test_name.lower())).order_by(sort_param)
    context = {
        'all_tests': tests,
        'test_url': test_name.replace(' ', '+'),
        'test_title': test_name,
        'sort_param': sort_param
    }
    return render(request, 'testik/search.html', context)


@login_required
def sort_tests(request):
    pass


@login_required
def test_preview(request, test_id):
    test = Test.objects.get(pk=test_id)
    context = {'test': test}
    return render(request, "testik/test_preview.html", context)


@login_required
def passing_test(request, test_id):
    test = Test.objects.get(pk=test_id)
    questions = Question.objects.filter(test_id=test_id)
    questions = questions.order_by('?') if test.shuffle else questions
    context = {'test': test, 'questions': questions}
    return render(request, "testik/passing.html", context)


@login_required
def result(request, test_id):
    if request.method == "POST":
        test = Test.objects.get(pk=test_id)
        test.attempts += 1
        test.save()
        total, maximum, mistakes = processing_user_answers(request, test_id)
        res = ceil(total / maximum * 100) if maximum != 0 else 100
        TestResult.objects.create(user_id=request.user, test_id=test,
                                  result=res, attempt_time=datetime.now())
        context = {'test': test, 'total': total, 'maximum': maximum, 'mistakes': mistakes, 'result': res}
    else:
        return redirect('/tests')
    return render(request, "testik/result.html", context)


@login_required
def history(request):
    results = TestResult.objects.filter(user_id=request.user.id)
    context = {"results": results}
    return render(request, "testik/history.html", context)
