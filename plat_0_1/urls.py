"""plat_0_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from plat_app_0_1 import views
urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('search_name/', views.search_name),
    path('lt_est/', views.lt_est),
    path('dau_est/', views.dau_est),
    path('dnu_est/', views.dnu_est),
    path('lt_est_cal/', views.lt_est_cal),
    path('dau_est_cal/', views.dau_est_cal),
    path('dnu_est_cal/', views.dnu_est_cal),
    path('cost_input/', views.cost_input),
    path('cost_input_submit/', views.cost_input_sumit),
]
