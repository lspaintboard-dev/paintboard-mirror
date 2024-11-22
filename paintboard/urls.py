"""paintboard URL Configuration

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
from django.urls import path
from index import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('paintboard/board/', views.getboard),
    path('paintboard/board', views.getboard),
    path('paintboard/boardimg', views.getboardasimg),
    path('paintboard/boardimg/', views.getboardasimg),
    path('paintboard/paint/', views.paintboard),
    path('paintboard/paint', views.paintboard),
    path('paintboard/gettoken', views.gettk),
    path('paintboard/gettoken/', views.gettk),
    path('paintboard/banip', views.banip),
    path('paintboard/banip/', views.banip),
    path('paintboard/unbanip', views.unbanip),
    path('paintboard/unbanip/', views.unbanip),
    path('paintboard/banuid', views.banuid),
    path('paintboard/banuid/', views.banuid),
    path('paintboard/unbanuid', views.unbanuid),
    path('paintboard/unbanuid/', views.unbanuid),
    path('paintboard/fill', views.fill),
    path('paintboard/fill/', views.fill),
    path('paintboard/fillimg', views.fillimg),
    path('paintboard/fillimg/', views.fillimg),
    path('paintboard/paintboard', views.index),
    path('paintboard/paintboard/', views.index),
    path('paintboard/errcnt', views.ret_cnt),
    path('paintboard/errcnt/', views.ret_cnt),
    path('paintboard/querypaint', views.querypaint),
    path('paintboard/querypaint/', views.querypaint),
    path('paintboard/createtoken', views.createtoken),
    path('paintboard/createtoken/', views.createtoken),
]
