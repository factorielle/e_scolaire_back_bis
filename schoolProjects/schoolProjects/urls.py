"""schoolProjects URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , re_path
from StudentApp.views import UserSignup, UserLogin , studentApi, LogoutView, eleve_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', UserSignup.as_view(), name='user-signup'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('eleve/', studentApi, name='crud-eleve'),
    re_path('eleve/(?P<pk>[0-9]+)$', eleve_detail, name='eleve-detail'),
]
