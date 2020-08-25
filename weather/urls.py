from django.urls import path
from .views import *

urlpatterns = [
    path('', show_results, name='shoe_results'),
]