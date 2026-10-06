from django.urls import path 
from .import views 


urlpatterns=[ 
    path('adminlogin',views.login,name='login'),
    path('adminhome',views.adminhome,name='adminhome')
]