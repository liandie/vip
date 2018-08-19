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
from django.db import connection
from ..models import Movies,Tvseries,Anime,Documentary,Videosum

def get_movies_main():
    info = list(Movies.objects.filter(moviessource='腾讯视频')[:48])
    return info

def get_tv_main():
    info = list(Tvseries.objects.filter(tvource='芒果Tv')[:24])
    return info

def get_anime_main():
    info = list(Anime.objects.filter(animeource='芒果Tv')[:24])
    return info

def get_documentary_main():
    info = list(Documentary.objects.filter(documentarysource='芒果Tv')[:6])
    return info


def get_movies(moviestype,moviesregion,moviesdecade,movieslanguage):
    info = list(Movies.objects.filter(moviestype__contains=moviestype,
    moviesregion__contains=moviesregion,moviesdecade__contains=moviesdecade,
    movieslanguage__contains=movieslanguage))
    # info.extend(list(Movies.objects.filter(moviessource__contains='')))
    return info

def get_anime(animetype,animeregion,animedecade,animelanguage):
    info = list(Anime.objects.filter(animetype__contains=animetype,
    animeregion__contains=animeregion,animedecade__contains=animedecade,
    animelanguage__contains=animelanguage))
    # info.extend(list(Movies.objects.filter(moviessource__contains='')))
    return info
def get_tv(tvtype,tvregion,tvdecade,tvlanguage):
    info = list(Tvseries.objects.filter(tvtype__contains=tvtype,
    tvregion__contains=tvregion,tvdecade__contains=tvdecade,
    tvlanguage__contains=tvlanguage))
    # info.extend(list(Movies.objects.filter(moviessource__contains='')))
    return info
def get_documentary(documentarytype,documentaryregion,documentarydecade,documentarylanguage):
    info = list(Documentary.objects.filter(documentarytype__contains=documentarytype,
    documentaryregion__contains=documentaryregion,documentarydecade__contains=documentarydecade,
    documentarylanguage__contains=documentarylanguage))
    # info.extend(list(Movies.objects.filter(moviessource__contains='')))
    return info

def get_search(videosumname):
    info = list(Videosum.objects.filter(videosumname__contains=videosumname))
    return info
