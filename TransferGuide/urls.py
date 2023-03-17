from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('ClassInfos/', views.Info, name='Info'),
    path('accounts/logout/', views.logoutt, name='logout'),
    path('sisUpdate/<semester>/<page>/<subjectNum>/', views.sisUpdate, name='update'),
    path('displayUpdate/<semester>/<page>/<subjectNum>/', views.displayUpdate, name='update')
]
