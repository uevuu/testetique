from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page, name='main'),
    path('tests/', filter_tests, name='tests'),
    path('tests/category/<int:category_id>/', get_category, name='category'),
    path('tests/<int:test_id>/', description_test, name='test'),
    path('tests/<int:test_id>/preview', test_preview, name='preview'),
    path('tests/<int:test_id>/passing/', passing_test, name='passing'),
    path('tests/<int:test_id>/result/', result, name='result'),
    path('history/', history, name='history'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout')
]
