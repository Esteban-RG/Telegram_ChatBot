"""
URL configuration for Telegram_ChatBot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from oauth_app import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('login/',views.login, name='login'),
    path('callback/', views.callback, name='callback'),
    path('end/', views.end, name='end'),
    path('get-credentials/<str:user_id>/', views.get_credentials, name='get_credentials'),
]
