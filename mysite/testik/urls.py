from django.urls import path
from .views import main_page, description_test, history, result, passing_test, tests_page

urlpatterns = [
    path('', main_page),
    path('tests', tests_page),
    path('tests/description/', description_test),
    path('tests/passing/', passing_test),
    path('tests/result/', result),
    path('history/', history)
]
