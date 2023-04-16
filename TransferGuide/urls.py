from django.urls import path

from . import views


urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('accounts/logout/', views.logoutt, name='logout'),
    path('sisUpdate/<semester>/<page>/<subjectNum>/', views.sisUpdate, name='update'),
    path('displayUpdate/<semester>/<page>/<subjectNum>/', views.displayUpdate, name='update'),
    path('allCourses', views.CoursesViewAll.as_view(), name='allCourses'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('info/', views.CourseInfo.as_view(), name='course_info'),
    path('filter/', views.CourseFilter.as_view(), name='course_filter'),
    path('addEquivalentCourse/', views.addEquivCourse, name='addEquivCoursePage'),
    path('requestForm/', views.RequestForms.as_view(), name='student_request'),
    path('requestForm/database', views.requests_database, name='dataForRequests'),
    path('pendingRequests/', views.pending_requests, name='pendingRequests'),
    path('mailBox/', views.mail_box, name='mailBox'),
    path('update_email_status/<int:email_id>/', views.update_email_status, name='update_email_status'),
    path('sendMail/', views.send_email, name='sendEmail'),
    path('sendMail/database', views.email_database, name='dataforEmails'),
    # path('autoDatabase', views.autoEmail_database, name='dataforAutoEmails'),
    # path('test/', views.ChangePriv.as_view(), name="test"),
    # path('change_superuser_status/', views.change_superuser_status, name='change_superuser_status'),
]
