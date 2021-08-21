from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login',views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('registerUser', views.registerUser, name='registerUser'),
    path('insertUser', views.insertUser, name='insertUser'),
    path('uploadsheet', views.uploadsheet, name='uploadsheet'),
    path('addtransaction', views.addtransaction, name='addtransaction'),
    path('admineditprofile', views.admineditprofile, name='admineditprofile'),
    path('admindashboard', views.admindashboard, name='admindashboard'),
    path('viewhistory', views.viewhistory, name='viewhistory'),
    path('viewusers', views.viewusers, name='viewusers'),
    path('edituser', views.edituser, name='edituser'),
    path('updateuser', views.updateuser, name='updateuser'),
    path('insertSheet', views.insertSheet, name='insertSheet'),
    path('editprofile', views.editprofile, name='editprofile'),
    path('agentdashboard', views.agentdashboard, name='agentdashboard'),
    path('agentupdatetransaction', views.agentupdatetransaction, name='agentupdatetransaction'),
    path('agentviewtransactions', views.agentviewtransactions, name='agentviewtransactions'),
    path('agentviewcustomers',views.agentviewcustomers, name='agentviewcustomers'),
    path('agentaddcustomer', views.agentaddcustomer, name='agentaddcustomer'),
    path('agenteditprofile', views.agenteditprofile, name='agenteditprofile'),
    path('agentprofile',views.agentprofile, name='agentprofile'),

]