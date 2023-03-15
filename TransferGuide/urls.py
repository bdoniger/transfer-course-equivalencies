from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('ClassInfos/', views.Info, name='Info'),
    path('accounts/logout1/', views.logoutt, name='logout')
]