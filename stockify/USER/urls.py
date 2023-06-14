from django.urls import path
from . import views

urlpatterns =[
    path('',views.home,name ='home'),
    path('register/',views.register, name='register'),
    path('login/',views.login_page,name ='login'),
    path('profile/',views.profile,name ='profile'),
    path('logout/',views.logout_page,name='logout'),
    path('profile_update/',views.profile_update,name='profile_update')

]