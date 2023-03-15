from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('ClassInfos/', views.Info, name='Info'),
]