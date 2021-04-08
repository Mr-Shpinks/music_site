from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
    url(r'^register/$', views.register, name='register'),
]
