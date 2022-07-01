from django.urls import path
from .views import main_page, description_test, history, result, passing_test

urlpatterns = [
    path('', main_page),
    path('description/', description_test),
    path('passing/', passing_test),
    path('result/', result),
    path('history/', history)
]
