from django.urls import path 
from .import views 

urlpatterns=[ 
    path('',views.home,name='home'),
    path('register',views.register,name='reg'),
    path('login',views.login,name='log'),
    path('stress',views.stress,name='stress'),
    path('predict',views.predict,name='predict'),
    path('logout',views.logout,name='logout')
]