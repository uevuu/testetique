from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .forms import UserRegisterForm, UserLoginForm
from .models import TestResult, Test, Category, Question


def main_page(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect("tests")
        else:
            messages.error(request, "Неудачная попытка регистрации")
    else:
        form = UserRegisterForm()
    content = {'form': form,
               'form_title': "Регистрация",
               "button_title": "Зарегистрироваться"}
    return render(request, template_name='testik/main_page.html', context=content)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tests')
    else:
        form = UserLoginForm()
    content = {'form': form,
               'form_title': "Авторизация",
               "button_title": "Авторизоваться"}
    return render(request, template_name='testik/main_page.html', context=content)


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
    return render(request, template_name='testik/tests_page.html', context=context)


@login_required
def get_category(request, category_id):
    child_category = Category.objects.filter(parent_id=category_id)
    if len(request.GET.getlist("sort_param")) == 0:
        sort_param = "-created_date"
    else:
        sort_param = request.GET.getlist("sort_param")[0]
    print(request.GET.getlist("sort_param"))
    all_tests = Test.objects.filter(Q(category_id__in=child_category) | Q(category_id=category_id)).order_by(sort_param)
    curr_category = Category.objects.get(pk=category_id)
    context = {
        'all_tests': all_tests,
        'category': curr_category,
        'sort_param': sort_param
    }
    return render(request, template_name='testik/category.html', context=context)


@login_required
def description_test(request, test_id):
    curr_test = get_object_or_404(Test, pk=test_id)
    questions = Question.objects.filter(test_id=test_id)
    context = {
        'test': curr_test,
        'questions': questions
    }
    return render(request, template_name='testik/test.html', context=context)


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
        return render(request, template_name='testik/tests_page.html', context=context)
    return tests_page(request)


# def index(request):
#     user_search = request.GET.get('search')
#     tests = Test.objects.filter(Q(description__icontains=user_search) | Q(title__icontains=user_search))
#     context = {'all_tests': tests}
#     return render(request, template_name='testik/tests_page.html', context=context)

@login_required
def sort_tests(request):
    pass


@login_required
def passing_test(request):
    return HttpResponse('Пользователь делает тест')


@login_required
def result(request):
    return HttpResponse('Твой результат')


@login_required
def history(request):
    results = TestResult.objects.filter(user_id=request.user.id)
    context = {"results": results}
    return render(request, template_name="testik/history.html", context=context)
