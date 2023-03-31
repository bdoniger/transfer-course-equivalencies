from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('ClassInfos/', views.Info, name='Info'),
    path('accounts/logout/', views.logoutt, name='logout'),
    path('sisUpdate/<semester>/<page>/<subjectNum>/', views.sisUpdate, name='update'),
    path('displayUpdate/<semester>/<page>/<subjectNum>/', views.displayUpdate, name='update'),
    path('allCourses', views.CoursesViewAll.as_view(), name='allCourses'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('info/', views.CourseInfo.as_view(), name='course_info'),
    path('filter/', views.CourseFilter.as_view(), name='course_filter'),
    path('requestForm/', views.RequestForms.as_view(), name='student_request'),
    path('requestForm/database', views.Requestsdatabase, name='dataForRequests')
]
