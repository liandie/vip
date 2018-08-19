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

from django.db import models

# Create your models here.

class Movies(models.Model):  # 电影表
    moviesname = models.CharField(verbose_name='电影名', db_index = True, max_length=49, unique=True)  #电影名
    moviessource = models.CharField(verbose_name='电影源', max_length=9, null=True, blank=True)  # 视频源
    moviesgrade =  models.CharField(verbose_name='电影等级', max_length=9, null=True, blank=True)  # 视频等级
    movieslanguage = models.CharField(verbose_name='电影语言', max_length=9, null=True, blank=True)  # 电影语言
    moviestype = models.CharField(verbose_name='电影类型', max_length=36, null=True, blank=True)  # 电影类型
    moviesdecade = models.CharField(verbose_name='电影年代', max_length=16, null=True, blank=True)  # 电影年代
    moviesregion = models.CharField(verbose_name='电影地区', max_length=25, null=True, blank=True)  # 电影地区
    pdatetime =  models.CharField(verbose_name='更新时间', max_length=16,  null=True,blank=True)  # 更新时间
    moviesimageurl = models.CharField(verbose_name='显示图片路径',  max_length=360, null=True,blank=True)  # 显示图片路径
    moviesurl = models.CharField(verbose_name='视频链接接口', max_length=100,null=True,blank=True)  # 视频破解链接接口集合
    moviesurl2 = models.TextField(verbose_name='视频破解链接', null=True,blank=True)  # 视频破解链接
    def __str__(self):
        return self.moviesname

class Tvseries(models.Model):  # 电视剧表
    tvname = models.CharField(verbose_name='电视名', db_index = True, max_length=49, unique=True)  #电视名
    tvource = models.CharField(verbose_name='电视源', max_length=16, null=True, blank=True, default='')  # 视频源
    tvcount = models.IntegerField(verbose_name='目前更新集数', default=0, null=True, blank=True)
    tvgrade =  models.CharField(verbose_name='电视等级', max_length=12,  default='', null=True, blank=True)  # 电视等级
    tvlanguage = models.CharField(verbose_name='电视语言', max_length=25, null=True, blank=True, default='')  # 电视语言
    tvtype = models.CharField(verbose_name='电视类型', max_length=49, null=True, blank=True, default='')  # 电视类型
    tvdecade = models.CharField(verbose_name='电视年代', max_length=16, null=True, blank=True, default='')  # 电视年代
    tvregion = models.CharField(verbose_name='电视地区', max_length=49, null=True, blank=True, default='')  # 电视地区
    pdate =  models.CharField(verbose_name='更新时间', max_length=16,  null=True,blank=True)  # 更新时间
    tvimageurl = models.CharField(verbose_name='显示图片路径',  max_length=360, null=True,blank=True)  # 显示图片路径
    tvurl = models.TextField(verbose_name='电视链接接口集合',  null=True,blank=True, default='')  # 电视破解链接接口集合
    tvurl2 = models.TextField(verbose_name='电视破解链接',  null=True,blank=True, default='')  # 电视破解链接

class Anime(models.Model):
    animename = models.CharField(verbose_name='电视名', db_index = True, max_length=49, unique=True)  #电视名
    animeource = models.CharField(verbose_name='电视源', max_length=16, null=True, blank=True, default='')  # 视频源
    animecount = models.IntegerField(verbose_name='目前更新集数', default=0, null=True, blank=True)
    animegrade =  models.CharField(verbose_name='电视等级', max_length=12,  default='', null=True, blank=True)  # 电视等级
    animelanguage = models.CharField(verbose_name='电视语言', max_length=25, null=True, blank=True, default='')  # 电视语言
    animetype = models.CharField(verbose_name='电视类型', max_length=49, null=True, blank=True, default='')  # 电视类型
    animedecade = models.CharField(verbose_name='电视年代', max_length=16, null=True, blank=True, default='')  # 电视年代
    animeregion = models.CharField(verbose_name='电视地区', max_length=49, null=True, blank=True, default='')  # 电视地区
    pdate =  models.CharField(verbose_name='更新时间', max_length=16,  null=True,blank=True)  # 更新时间
    animeimageurl = models.CharField(verbose_name='显示图片路径',  max_length=360, null=True,blank=True)  # 显示图片路径
    animeurl = models.TextField(verbose_name='电视链接接口集合',  null=True,blank=True, default='')  # 电视破解链接接口集合
    animeurl2 = models.TextField(verbose_name='电视破解链接',  null=True,blank=True, default='')  # 电视破解链接


class Documentary(models.Model):
    documentaryname = models.CharField(verbose_name='纪录片名', db_index = True, max_length=49, unique=True)  #纪录片名
    documentarysource = models.CharField(verbose_name='纪录片源', max_length=16, null=True, blank=True, default='')  # 视频源
    documentarycount = models.IntegerField(verbose_name='目前更新集数', default=0, null=True, blank=True)
    documentarygrade =  models.CharField(verbose_name='电视等级', max_length=12,  default='', null=True, blank=True)  # 电视等级
    documentarylanguage = models.CharField(verbose_name='纪录片语言', max_length=25, null=True, blank=True, default='')  # 纪录片语言
    documentarytype = models.CharField(verbose_name='纪录片类型', max_length=49, null=True, blank=True, default='')  # 纪录片类型
    documentarydecade = models.CharField(verbose_name='纪录片年代', max_length=16, null=True, blank=True, default='')  # 纪录片年代
    documentaryregion = models.CharField(verbose_name='纪录片地区', max_length=49, null=True, blank=True, default='')  # 纪录片地区
    pdatetime =  models.CharField(verbose_name='更新时间', max_length=16,  null=True,blank=True)  # 更新时间
    documentaryimageurl = models.TextField(verbose_name='显示图片路径',  null=True,blank=True, default='')  # 显示图片路径
    documentaryurl = models.TextField(verbose_name='电视链接接口集合',  null=True,blank=True, default='')  # 电视破解链接接口集合
    documentaryurl2 = models.TextField(verbose_name='电视破解链接',  null=True,blank=True, default='')  # 电视破解链接

class Videosum(models.Model):
    videosumname = models.CharField(verbose_name='电视名', db_index = True, max_length=49, unique=True)  #电视名
    videosumource = models.CharField(verbose_name='电视源', max_length=16, null=True, blank=True, default='')  # 视频源
    videosumcount = models.IntegerField(verbose_name='目前更新集数', default=0, null=True, blank=True)
    videosumgrade =  models.CharField(verbose_name='电视等级', max_length=12,  default='', null=True, blank=True)  # 电视等级
    videosumlanguage = models.CharField(verbose_name='电视语言', max_length=25, null=True, blank=True, default='')  # 电视语言
    videosumtype = models.CharField(verbose_name='电视类型', max_length=49, null=True, blank=True, default='')  # 电视类型
    videosumdecade = models.CharField(verbose_name='电视年代', max_length=16, null=True, blank=True, default='')  # 电视年代
    videosumregion = models.CharField(verbose_name='电视地区', max_length=49, null=True, blank=True, default='')  # 电视地区
    videosumimageurl = models.CharField(verbose_name='显示图片路径',  max_length=360, null=True,blank=True)  # 显示图片路径
    videosumurl = models.TextField(verbose_name='电视链接接口集合',  null=True,blank=True, default='')  # 电视破解链接接口集合
    videosumurl2 = models.TextField(verbose_name='电视破解链接',  null=True,blank=True, default='')
    pdatetime = models.CharField(verbose_name='更新时间', max_length=16,  null=True,blank=True)  # 更新时间
