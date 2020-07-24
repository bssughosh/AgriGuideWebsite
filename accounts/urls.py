from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('login/<str:ph>/', login1, name='login1'),
    path('register/', reg_state, name='reg_state'),
    path('register/<str:state>/', forward_state, name='forward_state'),
    path('register/<str:state>/<str:dist>/', reg1, name='reg1'),
]
