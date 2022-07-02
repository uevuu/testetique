from django.urls import path
from .views import main_page, description_test, history, result, passing_test, tests_page, get_category

urlpatterns = [
    path('', main_page, name='main'),
    path('tests', tests_page, name='tests'),
    path('tests/category/<int:category_id>/', get_category, name='category'),
    path('tests/description/', description_test, name='description'),
    path('tests/passing/', passing_test, name='passing'),
    path('tests/result/', result, name='result'),
    path('history/', history, name='history')
]
