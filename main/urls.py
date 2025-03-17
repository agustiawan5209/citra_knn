from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.main, name='home'),
    path('login/app', views.login, name='login.app'),
    path('register/app', views.register, name='register.app'),
]
