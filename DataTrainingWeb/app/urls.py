from django.conf.urls import url

from . import views

app_name = 'app'

urlpatterns = [
    #Views
    url(r'^index', views.loginView, name='login'),
    url(r'^managestudent', views.manageStudentView, name='manageStudent'),
    # url(r'^stdlist', views.stdListView, name='stdList'),
    # url(r'^home', views.homeView, name='home'),
    url(r'^training', views.trainingView, name='training'),
    url(r'^appadmin', views.adminView, name='appAdmin'),
    url(r'^managegroup', views.manageGroupView, name='manageGroup'),
    url(r'^training', views.trainingView, name='training'),
    #Actions
    url(r'^home', views.doLogin, name='doLogin'),
    url(r'^registered', views.addStudent, name='addStudent'),
    url(r'^studentupdated', views.updateStudent, name='updateStudent'),
    url(r'^studentdeleted', views.deleteStudent, name='deleteStudent'),
    url(r'^groupdeleted', views.deleteGroup, name='deleteGroup'),
    url(r'^index', views.doLogout, name='doLogout'),
    url(r'^registerd', views.addGroup, name='addGroup'),
    url(r'^selectgroup', views.selectGroup, name='selectGroup'),
]
