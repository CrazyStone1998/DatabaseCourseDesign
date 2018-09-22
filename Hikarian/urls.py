# coding=utf-8
from django.contrib import admin
from django.urls import re_path,include,path
from Hikarian import views
app_name = 'Hikarian'
urlpatterns = [

    re_path(r'^hasLoggedIn/*$',     views.hasLoggedIn,    name='hasLoggedIn'),
    re_path(r'^login/*$',           views.login,          name='login'),
    re_path(r'^logout/*$',          views.logout,         name='logout'),
    re_path(r'^register/*$',        views.register,       name='register'),
    re_path(r'^user/*$',            views.user_splitter, {'GET': views.userGET, 'POST': views.userPOST}, name='user'),
    re_path(r'^searchdirect/*$',    views.searchdirect,   name='searchdirect'),
    re_path(r'^searchtransfer/*$',  views.searchtransfer, name='searchtransfer'),
    re_path(r'^refund/*$',          views.refund,         name='refund'),
    re_path(r'^prelot/*$',          views.prelot,         name='prelot'),
    re_path(r'^order/*$',           views.order,          name='order'),
    re_path(r'^change/*$',          views.change,         name='change'),
    re_path(r'^pay/*$',             views.pay,            name='pay'),
    re_path(r'^recharge/*$',        views.recharge,       name='recharge'),



]
