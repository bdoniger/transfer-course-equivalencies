from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('ClassInfos/', views.Info, name='Info'),
    path('accounts/logout/', views.logoutt, name='logout'),
    path('sisUpdate/', views.sisUpdate, name='update')
]