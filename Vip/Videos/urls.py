#!/usr/bin/env python
# encoding: utf-8
"""
@version: python3.6.5
@author: myyao
@license: python
@contact: longzinziyan@gmail.com
@software: PyCharm
@file: views.py
@time: 2018/4/13 20:37
"""
from django.conf.urls import url
from .import views 

handler403 = views.page_error
handler404 = views.page_error
handler500 = views.page_error


urlpatterns = [
    url(r'^ceshi$',views.ceshi,name='ceshi'),
    url(r'^quan$',views.quan,name='quan'),
    url(r'^video$',views.video,name='video'),
    url(r'^main$',views.main,name='main'),
    url(r'^movie$',views.movie,name='movie'),
    url(r'^anime$',views.anime,name='anime'),
    url(r'^tv$',views.tv,name='tv'),
    url(r'^documentary$',views.documentary,name='documentary'),
    url(r'^show$',views.show,name='show'),
    url(r'^search$',views.search,name='search'),
    url(r'^pageindex/',views.pageindex,name='pageindex'),
    url(r'^playing(\d+)type(\d+)',views.playing,name='playing'),
    url(r'^ceshi$',views.ceshi,name='ceshi'),
]
