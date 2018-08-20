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
# import requests
# from bs4 import BeautifulSoup
# from selenium import webdriver
# import re
# from django.db import connection
from Videos import models
from .Database.Mgtv import *
from .Database.Tx import *
from .Database.Db import *
from .Database.Youku import *
import re
import json
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from .models import Movies,Anime,Tvseries,Videosum
from django.utils.datastructures import MultiValueDictKeyError



def page_error(request):
    return render(request, '404.html')


def checkMobile(userAgent):
    _long_matches = r'googlebot-mobile|android|avantgo|blackberry|blazer|elaine|hiptop|ip(hone|od)|kindle|midp|mmp|mobile|o2|opera mini|palm( os)?|pda|plucker|pocket|psp|smartphone|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce; (iemobile|ppc)|xiino|maemo|fennec'
    _long_matches = re.compile(_long_matches, re.IGNORECASE)
    _short_matches = r'1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(' \
                     r'av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(' \
                     r'ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(' \
                     r'n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(' \
                     r'it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez(' \
                     r'[4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(' \
                     r'ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(' \
                     r'aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(' \
                     r't|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(' \
                     r'k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(' \
                     r'di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[' \
                     r'0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(' \
                     r'6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(' \
                     r'ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[' \
                     r'2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(' \
                     r'01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(' \
                     r'al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(' \
                     r'gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(' \
                     r'\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(' \
                     r'52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|xda(' \
                     r'\-|2|g)|yas\-|your|zeto|zte\- '
    _short_matches = re.compile(_short_matches, re.IGNORECASE)
    if _long_matches.search(userAgent) != None:
        return True
    user_agent = userAgent[0:4]
    if _short_matches.search(user_agent) != None:
        return True
    return False


def playing(request,id,typeid):
    texthtml = request.META.get('HTTP_USER_AGENT')
    if int(typeid) == 0:
        info = list(Movies.objects.filter(id=id))
        if checkMobile(texthtml):
            return render(request,'playing.html',{'device':'mobile','name':info[0].moviesname,'urlinfo':info[0],'urlnum':info[0].moviesurl,'typeid':typeid})
        else:
            return render(request,'playing.html',{'device':'computer','name':info[0].moviesname,'urlinfo':info[0],'urlnum':info[0].moviesurl,'typeid':typeid})
    elif int(typeid) == 1:
        info = list(Anime.objects.filter(id=id))
        dic = eval(info[0].animeurl)
        if checkMobile(texthtml):
            return render(request,'playing.html',{'device':'mobile','name':info[0].animename,'urlinfo':dic,'urlnum':dic[0]['url'],'typeid':typeid})
        else:
            return render(request,'playing.html',{'device':'computer','name':info[0].animename,'urlinfo':dic,'urlnum':dic[0]['url'],'typeid':typeid})
    elif int(typeid) == 2:
        info = list(Tvseries.objects.filter(id=id))
        dic = eval(info[0].tvurl)
        print(dic)
        if checkMobile(texthtml):
            return render(request,'playing.html',{'device':'mobile','name':info[0].tvname,'urlinfo':dic,'urlnum':dic[0]['url'],'typeid':typeid})
        else:
            return render(request,'playing.html',{'device':'computer','name':info[0].tvname,'urlinfo':dic,'urlnum':dic[0]['url'],'typeid':typeid})
    elif int(typeid) == 3:
        info = list(Documentary.objects.filter(id=id))
        dic = eval(info[0].documentaryurl)
        print(dic)
        if checkMobile(texthtml):
            return render(request,'playing.html',{'device':'mobile','name':info[0].documentaryname,'urlinfo':dic,'urlnum':dic[0]['url'],'typeid':typeid})
        else:
            return render(request,'playing.html',{'device':'computer','name':info[0].documentaryname,'urlinfo':dic,'urlnum':dic[0]['url'],'typeid':typeid})
    elif int(typeid) == 4:
        info = list(Videosum.objects.filter(id=id))
        if info[0].videosumcount > 0:
            dic = eval(info[0].videosumurl)
            print(dic)
            if checkMobile(texthtml):
                return render(request,'playing.html',{'device':'mobile','name':info[0].videosumname,'urlinfo':dic,'urlnum':dic[0]['url'],'typeid':4})
            else:
                return render(request,'playing.html',{'device':'computer','name':info[0].videosumname,'urlinfo':dic,'urlnum':dic[0]['url'],'typeid':4})
        else:
            info = list(Videosum.objects.filter(id=id))
            if checkMobile(texthtml):
                return render(request,'playing.html',{'device':'mobile','name':info[0].videosumname,'urlinfo':info[0],'urlnum':info[0].videosumurl,'typeid':0})
            else:
                return render(request,'playing.html',{'device':'computer','name':info[0].videosumname,'urlinfo':info[0],'urlnum':info[0].videosumurl,'typeid':0})
def movie(request):
    moviestype=''
    moviesregion=''
    moviesdecade=''
    movieslanguage=''
    page = '1'
    texthtml = request.META.get('HTTP_USER_AGENT')
    if request.method == 'GET':
        try:
            moviestype = request.GET['mode']
        except MultiValueDictKeyError as e:
            print('mode Erro')
        try:
            moviesregion = request.GET['stage']
        except MultiValueDictKeyError as e:
            print('mode Erro')
        try:
            moviesdecade = request.GET['sector']
        except MultiValueDictKeyError as e:
            print('mode Erro')
        try:
            movieslanguage = request.GET['board']
        except MultiValueDictKeyError as e:
            print('mode Erro')
        try:
            page = int(request.GET['page'])
        except MultiValueDictKeyError as e:
            print('mode Erro')
            page = int(page)
    elif request.method == 'POST':
        videosname = request.POST['form-control']
    # except MultiValueDictKeyError as e:
    movies = get_movies(moviestype,moviesregion,moviesdecade,movieslanguage)
    count = len(movies)
    dic={'moviestype':moviestype,'moviesregion':moviesregion,'moviesdecade':moviesdecade,'movieslanguage':movieslanguage}
    print('..............',count)
    if checkMobile(texthtml):
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<手机')
        return render(request,'videos/movie.html',{'device':'mobile','movies':movies[(page-1)*30:page*30],'dic':dic,'page':page,'count':count,'countpage':(count//30)+1})
    else:
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<电脑')
        return render(request,'videos/movie.html',{'device':'computer','movies':movies[(page-1)*30:page*30],'dic':dic,'page':page,'count':count,'countpage':(count//30)+1})


def pageindex(request):
    urltype = request.POST['urltype']
    mtype = request.POST['type']
    region = request.POST['region']
    decade = request.POST['decade']
    language = request.POST['language']
    pageupdn = request.POST['pageupdn']
    page = int(request.POST['page'])
    countpage = int(request.POST['countpage'])
    if urltype in 'anime':
        info = get_anime(mtype,region,decade,language)
    elif urltype in 'movie':
        info = get_movies(mtype,region,decade,language)
    elif urltype in 'tv':
        info = get_tv(mtype,region,decade,language)
    elif urltype in 'documentary':
        info = get_documentary(mtype,region,decade,language)
    if int(pageupdn) == 1:
        return_json = info[(int(page)-2)*30:(int(page)-1)*30]
        if page != 1:
            page -= 1
    elif int(pageupdn) == 0:
        return_json = info[(int(page))*30:(int(page)+1)*30]
        if page != countpage:
            page += 1
    print('.....................................',return_json)
    return HttpResponse(json.dumps({'info':return_json,'pagenum':page},default=lambda obj:obj.__dict__), content_type='application/json')

def anime(request):
    animetype=''
    animeregion=''
    animedecade=''
    animelanguage=''
    page = '1'
    texthtml = request.META.get('HTTP_USER_AGENT')
    if request.method == 'GET':
        try:
            animetype = request.GET['mode']
        except MultiValueDictKeyError as e:
            print('mode Erro')
        try:
            animeregion = request.GET['stage']
        except MultiValueDictKeyError as e:
            print('mode Erro')
        try:
            animedecade = request.GET['sector']
        except MultiValueDictKeyError as e:
            print('mode Erro')
        try:
            animelanguage = request.GET['board']
        except MultiValueDictKeyError as e:
            print('mode Erro')
        try:
            page = int(request.GET['page'])
        except MultiValueDictKeyError as e:
            print('mode Erro')
            page = int(page)
    elif request.method == 'POST':
        videosname = request.POST['form-control']
    # except MultiValueDictKeyError as e:
    anime = get_anime(animetype,animeregion,animedecade,animelanguage)
    count = len(anime)
    dic={'animetype':animetype,'animeregion':animeregion,'animedecade':animedecade,'animelanguage':animelanguage}
    if checkMobile(texthtml):
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<手机')
        return render(request,'videos/anime.html',{'device':'mobile','anime':anime[(page-1)*30:page*30],'dic':dic,'page':1,'count':count,'countpage':(count//30)+1})
    else:
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<电脑')
        return render(request,'videos/anime.html',{'device':'computer','anime':anime[(page-1)*30:page*30],'dic':dic,'page':1,'count':count,'countpage':(count//30)+1})

def tv(request):
    tvtype=''
    tvregion=''
    tvdecade=''
    tvlanguage=''
    page = '1'
    texthtml = request.META.get('HTTP_USER_AGENT')
    if request.method == 'GET':
        try:
            tvtype = request.GET['mode']
        except MultiValueDictKeyError as e:
            print('mode Erro')
        try:
            tvregion = request.GET['stage']
        except MultiValueDictKeyError as e:
            print('mode Erro')
        try:
            tvdecade = request.GET['sector']
        except MultiValueDictKeyError as e:
            print('mode Erro')
        try:
            tvlanguage = request.GET['board']
        except MultiValueDictKeyError as e:
            print('mode Erro')
        try:
            page = int(request.GET['page'])
        except MultiValueDictKeyError as e:
            print('mode Erro')
            page = int(page)
    elif request.method == 'POST':
        videosname = request.POST['form-control']
    # except MultiValueDictKeyError as e:
    tv = get_tv(tvtype,tvregion,tvdecade,tvlanguage)
    count = len(tv)
    dic={'tvtype':tvtype,'tvregion':tvregion,'tvdecade':tvdecade,'tvlanguage':tvlanguage}
    if checkMobile(texthtml):
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<手机')
        return render(request,'videos/tv.html',{'device':'mobile','tv':tv[(page-1)*30:page*30],'dic':dic,'page':1,'count':count,'countpage':(count//30)+1})
    else:
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<电脑')
        return render(request,'videos/tv.html',{'device':'computer','tv':tv[(page-1)*30:page*30],'dic':dic,'page':1,'count':count,'countpage':(count//30)+1})


def documentary(request):
    documentarytype=''
    documentaryregion=''
    documentarydecade=''
    documentarylanguage=''
    page = '1'
    texthtml = request.META.get('HTTP_USER_AGENT')
    if request.method == 'GET':
        try:
            documentarytype = request.GET['mode']
        except MultiValueDictKeyError as e:
            print('mode Erro')
        try:
            documentaryregion = request.GET['stage']
        except MultiValueDictKeyError as e:
            print('mode Erro')
        try:
            documentarydecade = request.GET['sector']
        except MultiValueDictKeyError as e:
            print('mode Erro')
        try:
            documentarylanguage = request.GET['board']
        except MultiValueDictKeyError as e:
            print('mode Erro')
        try:
            page = int(request.GET['page'])
        except MultiValueDictKeyError as e:
            print('mode Erro')
            page = int(page)
    elif request.method == 'POST':
        videosname = request.POST['form-control']
    # except MultiValueDictKeyError as e:
    documentary = get_documentary(documentarytype,documentaryregion,documentarydecade,documentarylanguage)
    count = len(documentary)
    dic={'documentarytype':documentarytype,'documentaryregion':documentaryregion,
    'documentarydecade':documentarydecade,'documentarylanguage':documentarylanguage}
    if checkMobile(texthtml):
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<手机')
        return render(request,'videos/documentary.html',{'device':'mobile','documentary':documentary[(page-1)*30:page*30],'dic':dic,'page':1,'count':count,'countpage':(count//30)+1})
    else:
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<电脑')
        return render(request,'videos/documentary.html',{'device':'computer','documentary':documentary[(page-1)*30:page*30],'dic':dic,'page':1,'count':count,'countpage':(count//30)+1})


def show(request):
    texthtml = request.META.get('HTTP_USER_AGENT')
    print('>>>>>>>>>>>>>>>>>>>>>>>',texthtml)
    if checkMobile(texthtml):
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<手机')
        return render(request,'videos/show.html',{'device':'mobile'})
    else:
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<电脑')
        return render(request,'videos/show.html',{'device':'computer'})

def search(request):
    searchname = ''
    texthtml = request.META.get('HTTP_USER_AGENT')
    print('>>>>>>>>>>>>>>>>>>>>>>>',texthtml)
    try:
        if request.method == 'GET':
            searchname = request.GET['form-control']
        elif request.method == 'POST':
            searchname = request.POST['form-control']
    except MultiValueDictKeyError as e:
        print('erro')
    videolist = get_search(searchname)
    if checkMobile(texthtml):
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<手机')
        return render(request,'videos/search.html',{'device':'mobile','videolist':videolist})
    else:
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<电脑')
        return render(request,'videos/search.html',{'device':'computer','videolist':videolist})

def main(request):
    movies=get_movies_main()
    anime=get_anime_main()
    tv=get_tv_main()
    documentary=get_documentary_main()
    texthtml = request.META.get('HTTP_USER_AGENT')
    print('>>>>>>>>>>>>>>>>>>>>>>>',len(movies))
    if checkMobile(texthtml):
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<手机')
        return render(request,'videos/main.html',{'device':'mobile','movies':movies,'anime':anime,'tv':tv,'documentary':documentary})
    else:
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<电脑')
        return render(request,'videos/main.html',{'device':'computer','movies':movies,'anime':anime,'tv':tv,'documentary':documentary})
def quan(request):
    print('准备开始更新............................................')
    name = ''
    type = ''
    try:
        if request.method == 'GET':
            name = request.GET['quan']
            type = request.GET['type']
    except MultiValueDictKeyError as e:
        print(e)
    print(name,type)
    if '芒果' in name:
        mgtv(type)
    elif '腾讯' in name:
        tx(type)
    elif '优酷' in name:
        youku(type)
    return HttpResponse('恭喜更新成功.................')

def video(request):
    return render(request,'video.html')


def ceshi(request):
    print('测试成功')
    print(int(""))
