#users/urls.py
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from users.views import Form

urlpatterns = [

 path('', views.home, name = "home"),
 #path('', views.home, name = "signup")
 path("signup/", views.SignUp.as_view(), name="signup"),
 path('form/', views.form, name="form"),
 path('add_user/', views.add_user, name="add_user"),
 path('url_input/', views.url_input, name="url_input"),
 path('url_is_valid/', views.url_is_valid, name="url_is_valid"),




]

urlpatterns += staticfiles_urlpatterns()
