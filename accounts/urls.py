from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('login/<str:ph>/', login1, name='login1'),
    path('deleter/<int:obj>/', deleter, name='deleter'),
    path('deleter1/<int:obj>/', deleter1, name='deleter1'),
    path('register/', reg_state, name='reg_state'),
    path('register/<str:state>/', forward_state, name='forward_state'),
    path('register/<str:state>/<str:dist>/', reg1, name='reg1'),
    path('register2/<int:obj>/', reg2, name='reg2'),
    path('register3/<int:obj>/', reg3, name='reg3'),
]
