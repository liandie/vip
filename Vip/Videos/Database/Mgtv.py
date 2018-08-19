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
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
from json import loads
from django.db import connection
from ..models import Movies,Tvseries,Anime

def mgtvmovies():
    flag = 0
    count = 0
    url = 'https://list.mgtv.com/3/a4-a3-------a7-2-%d--a1-.html?channelId=3'
    for i in range(1,75):
        flag += 1
        sum = 0
        print('..........................正在添加第%d页的信息.........................' %(flag))
        page = url %(i)
        driver = webdriver.Chrome()
        driver.set_window_size(1920, 1080)
        req = requests.get(page)
        soup = BeautifulSoup(req.text, 'lxml')
        html = soup.find_all(class_='m-result-list-item')
        for n in html:
            sum += 1
            count += 1
            print('>>>>>>>>>>>>>>>>>>>>>>>当前总共提取了 %d 条信息<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<' % (count))
            print('---------------------正在添加第 %d 页的第 %d 条信息------------------------' % (flag, sum))
            html_str = str(n)
            try:
                info = re.findall('<a class="u-video u-video-y" href="//(.*?)" onclick="javascript:_reportData', html_str, re.S)
            except IndexError as e:
                info.append('')
            try:
                info.append(re.findall('<img alt="(.*?)" class="u-pic" src="', html_str, re.S)[0])
            except IndexError as e:
                info.append('')
            try:
                info.append(re.findall('" class="u-pic" src="//(.*?)"/>', html_str, re.S)[0])
            except IndexError as e:
                info.append('')
            try:
                info.append(re.findall('<em class="u-meta">(.*?)</em>', html_str, re.S)[0])
            except IndexError as e:
                info.append('')
            try:
                info.append(re.findall('<i class="mark-v" style="background:.*;">(.*?)</i>', html_str, re.S)[0])
            except IndexError as e:
                info.append('')
            if not ('期' in info[3]) and not ('预告' in info[4]):
                if(len(Movies.objects.filter(moviesname=info[1]))<1):
                    driver.get('https://' + info[0])
                    new_html = driver.page_source
                    try:
                        info.append(re.findall('<span class="mes">上映：(.*?)</span>', new_html)[0])
                    except IndexError as e:
                        info.append('')
                    try:
                        info.append(re.findall('<span class="mes">类型：(.*?)</span>', new_html)[0])
                    except IndexError as e:
                        info.append('')
                    try:
                        info.append(re.findall('<span class="mes">语言：(.*?)</span>', new_html)[0])
                    except IndexError as e:
                        info.append('')
                    try:
                        di_qu = re.findall('<span class="label">地区：</span>(.*?)/a>', new_html, re.S)[0]
                    except IndexError as e:
                        di_qu = ''
                    try:
                        info.append(re.findall('target="_blank">(.*?)<', di_qu, re.S)[0])
                    except IndexError as e:
                        info.append('')
                    try:
                        info.append(re.findall('<span class="details">(.*?)</span>', new_html, re.S)[0])
                    except IndexError as e:
                        info.append('')
                    pf = 0.0
                    if info[3] != '':
                        pf = float(info[3])
                    movies = Movies(moviesname=info[1],moviestext=info[9],moviessource='芒果Tv',
                    moviesscore=pf,moviesgrade=info[4],movieslanguage=info[7],moviestype=info[6],
                    moviesdecade=info[5],moviesregion=info[8],visittoday=0,visitthisweek=0,
                    historyaccess=0,Playamount=0,pdatetime=info[5],moviesimageurl=info[2],
                    moviesurl=info[0],moviesurl2='[]')
                    movies.save()
                    print('++++++++++++++++成功的添加一条信息',info)
                else:
                    print('已经添加本条信息!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            info.clear()
        driver.close()

def mgtvtv():
    flag = 0
    countsum = 0
    driver = webdriver.Chrome()
    driver.set_window_size(888, 666)
    lg = {'内地': '普通话', '韩国': '韩语', '中国香港': '粤语', '中国台湾': '台语', '日本': '日语', '其他': '其他'}
    urll = 'https://list.mgtv.com/2/a4-a3--------2-%d--a1-.html?channelId=2'
    for ii in range(1,28):
        flag += 1
        sum = 0
        print('..........................正在添加第%d页的信息.........................' %(flag))
        page = urll %(ii)
        req = requests.get(page)
        soup = BeautifulSoup(req.text, 'lxml')
        html = soup.find_all(class_='m-result-list-item')
        for n in html:
            sum += 1
            countsum += 1
            print('>>>>>>>>>>>>>>>>>>>>>>>当前总共提取了 %d 条信息<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<' % (countsum))
            print('---------------------正在添加第 %d 页的第 %d 条信息------------------------' % (flag, sum))
            if countsum >= 1:
                html_str = str(n)
                try:
                    info = re.findall('<a class="u-video u-video-y" href="//(.*?)" onclick="javascript:_reportData', html_str, re.S)
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('<img alt="(.*?)" class="u-pic" src="', html_str, re.S)[0])
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('" class="u-pic" src="//(.*?)"/>', html_str, re.S)[0])
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('<em class="u-meta">(.*?)</em>', html_str, re.S)[0])
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('<i class="mark-v" style="background:.*;">(.*?)</i>', html_str, re.S)[0])
                except IndexError as e:
                    info.append('')
                if not ('期' in info[3]) and not ('预告' in info[4]):
                    count = 0
                    try:
                        count_str = re.findall('(\d+)', info[3], re.S)[0]
                    except IndexError as e:
                        count_str = ''
                    if count_str != '':
                        count = int(count_str)
                    tv = Tvseries.objects.filter(tvname=info[1])
                    if(len(tv)<1):
                        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>https://' + info[0])
                        driver.get('https://' + info[0])
                        new_html = driver.page_source
                        try:
                            di_qu = re.findall('<span class="label">地区：</span>(.*?)/a>', new_html, re.S)[0]
                        except IndexError as e:
                            di_qu = ''
                        try:
                            info.append(re.findall('target="_blank">(.*?)<', di_qu, re.S)[0])
                            try:
                                info.append(lg[info[5]])
                            except KeyError as e:
                                info.append('其他')
                        except IndexError as e:
                            info.append('无')
                        try:
                            le = re.findall('target="_blank">(.*?)</a>', re.findall('<span class="label">类型：</span>(.*?)</p>', new_html, re.S)[0], re.S)
                            le_str = ''
                            for i in le:
                                le_str += i
                            info.append(le_str)
                        except IndexError as e:
                            info.append('')
                        try:
                            info.append(re.findall('<span class="details">(.*?)</span>', new_html, re.S)[0])
                        except IndexError as e:
                            info.append('')
                        try:
                            video_id = re.findall('www.mgtv.com/.*/.*/(.*?).html', info[0])
                            url = 'https://pcweb.api.mgtv.com/episode/list?video_id=%s&page=%d&size=25'
                        except IndexError as e:
                            url = 'https://www.baidu.com?dd=%s&aa=%d'
                        list_str = '['
                        for l in range(1,(count//25)+2):
                            vi_req = requests.get(url % (video_id[0],l))
                            json = loads(vi_req.text)
                            for nn in json['data']['list']:
                                if not (nn['isnew'] in '2'):
                                    list_str += '{"di":' + nn['t1'] + ',"tm":"' + nn['ts'] + '","title":"' + nn[
                                        't2'] + '","url":"https://www.mgtv.com'
                                    list_str += nn['url'] + '","img":"' + nn['img'] + '"},'
                        list_str = list_str[:-1] + ']'
                        try:
                            info.append(json['data']['count'])
                        except IndexError as e:
                            info.append('')
                        try:
                            info.append(json['data']['list'][0]['ts'][:10])
                        except IndexError as e:
                            info.append('')
                        info.append(list_str)
                        tvseries = Tvseries(tvname=info[1],tvtext=info[8],tvource='芒果Tv',
                        tvid=video_id,tvepisode=info[3],tvcount=info[9],tvgrade=info[4],
                        tvlanguage=info[6],tvtype=info[7],tvdecade=info[10],
                        tvregion=info[5],visittoday=0,visitthisweek=0,historyaccess=0,Playamount=0,
                        pdate=info[10],tvimageurl=info[2],tvurl=info[11],tvurl2='[]')
                        tvseries.save()
                        print('成功的添加一条信息+++++++++++++++++++++++++++++++++++++++++++++++++++')
                        print(info[:10])
                    elif tv[0].tvcount < count:
                        try:
                            video_id = re.findall('www.mgtv.com/.*/.*/(.*?).html', info[0])
                            url = 'https://pcweb.api.mgtv.com/episode/list?video_id=%s&page=%d&size=25'
                        except IndexError as e:
                            url = 'https://www.baidu.com?dd=%s&aa=%d'
                        list_str = '['
                        for l in range(1,(count//25)+2):
                            vi_req = requests.get(url % (video_id[0],l))
                            json = loads(vi_req.text)
                            for nn in json['data']['list']:
                                if not (nn['isnew'] in '2'):
                                    list_str += '{"di":' + nn['t1'] + ',"tm":"' + nn['ts'] + '","title":"' + nn[
                                        't2'] + '","url":"https://www.mgtv.com'
                                    list_str += nn['url'] + '","img":"' + nn['img'] + '"},'
                        list_str = list_str[:-1] + ']'
                        tv.update(tvurl=list_str,tvcount=count)
                        print('更新视频信息.......................................................')
                        print(info)
                    else:
                        print('已经添加本条信息!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        print(info)
                info.clear()
    driver.close()

def mgtvanime():
    flag = 0
    countsum = 0
    driver = webdriver.Chrome()
    driver.set_window_size(888, 666)
    lg = {'美国':'英语','英国':'英语','法国':'法语','内地': '普通话', '韩国': '韩语', '中国香港': '粤语', '中国台湾': '台语', '日本': '日语', '其他': '其他'}
    urll = 'https://list.mgtv.com/50/-a3--a6-----a7-2-%d---.html?channelId=50'
    for ii in range(1,28):
        flag += 1
        sum = 0
        print('..........................正在添加第%d页的信息.........................' %(flag))
        page = urll %(ii)
        req = requests.get(page)
        soup = BeautifulSoup(req.text, 'lxml')
        html = soup.find_all(class_='m-result-list-item')
        for n in html:
            sum += 1
            countsum += 1
            print('>>>>>>>>>>>>>>>>>>>>>>>当前总共提取了 %d 条信息<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<' % (countsum))
            print('---------------------正在添加第 %d 页的第 %d 条信息------------------------' % (flag, sum))
            if countsum >= 1:
                html_str = str(n)
                try:
                    info = re.findall('<a class="u-video u-video-y" href="//(.*?)" onclick="javascript:_reportData', html_str, re.S)
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('<img alt="(.*?)" class="u-pic" src="', html_str, re.S)[0])
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('" class="u-pic" src="//(.*?)"/>', html_str, re.S)[0])
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('<em class="u-meta">(.*?)</em>', html_str, re.S)[0])
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('<i class="mark-v" style="background:.*;">(.*?)</i>', html_str, re.S)[0])
                except IndexError as e:
                    info.append('')
                if not ('期' in info[3]) and not ('预告' in info[4]):
                    count = 0
                    try:
                        count_str = re.findall('(\d+)', info[3], re.S)[0]
                    except IndexError as e:
                        count_str = ''
                    if count_str != '':
                        count = int(count_str)
                    anime = Anime.objects.filter(animename=info[1])
                    if(len(anime)<1):
                        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>https://' + info[0])
                        driver.get('https://' + info[0])
                        new_html = driver.page_source
                        try:
                            di_qu = re.findall('<span class="label">地区：</span>(.*?)/a>', new_html, re.S)[0]
                        except IndexError as e:
                            di_qu = ''
                        try:
                            info.append(re.findall('target="_blank">(.*?)<', di_qu, re.S)[0])
                            try:
                                info.append(lg[info[5]])
                            except KeyError as e:
                                info.append('其他')
                        except IndexError as e:
                            info.append('无')
                        try:
                            le = re.findall('target="_blank">(.*?)</a>', re.findall('<span class="label">类型：</span>(.*?)</p>', new_html, re.S)[0], re.S)
                            le_str = ''
                            for i in le:
                                le_str += i
                            info.append(le_str)
                        except IndexError as e:
                            info.append('')
                        try:
                            info.append(re.findall('<span class="details">(.*?)</span>', new_html, re.S)[0])
                        except IndexError as e:
                            info.append('')
                        try:
                            video_id = re.findall('www.mgtv.com/.*/.*/(.*?).html', info[0])
                            url = 'https://pcweb.api.mgtv.com/episode/list?video_id=%s&page=%d&size=25'
                        except IndexError as e:
                            url = 'https://www.baidu.com?dd=%s&aa=%d'
                        try:
                            list_str = '['
                            for l in range(1,(count//25)+2):
                                vi_req = requests.get(url % (video_id[0],l))
                                json = loads(vi_req.text)
                                for nn in json['data']['list']:
                                    if not (nn['isnew'] in '2'):
                                        list_str += '{"di":' + nn['t1'] + ',"tm":"' + nn['ts'] + '","title":"' + nn[
                                            't2'] + '","url":"https://www.mgtv.com'
                                        list_str += nn['url'] + '","img":"' + nn['img'] + '"},'
                            list_str = list_str[:-1] + ']'
                            try:
                                info.append(json['data']['count'])
                            except KeyError as e:
                                info.append('')
                            try:
                                info.append(json['data']['list'][0]['ts'][:10])
                            except IndexError as e:
                                info.append('')
                            info.append(list_str)
                            anime = Anime(animename=info[1],animetext=info[8],animeource='芒果Tv',
                            animeid=video_id,animeepisode=info[3],animecount=info[9],animegrade=info[4],
                            animelanguage=info[6],animetype=info[7],animedecade=info[10],
                            animeregion=info[5],visittoday=0,visitthisweek=0,historyaccess=0,Playamount=0,
                            pdate=info[10],animeimageurl=info[2],animeurl=info[11],animeurl2='[]')
                            anime.save()
                            print('成功的添加一条信息+++++++++++++++++++++++++++++++++++++++++++++++++++')
                            print(info[:10])
                        except KeyError as e:
                            info.append('')
                            info.append('')
                            info.append('[]')
                    elif anime[0].animecount < count:
                        try:
                            video_id = re.findall('www.mgtv.com/.*/.*/(.*?).html', info[0])
                            url = 'https://pcweb.api.mgtv.com/episode/list?video_id=%s&page=%d&size=25'
                        except IndexError as e:
                            url = 'https://www.baidu.com?dd=%s&aa=%d'
                        try:
                            list_str = '['
                            for l in range(1,(count//25)+2):
                                vi_req = requests.get(url % (video_id[0],l))
                                json = loads(vi_req.text)
                                for nn in json['data']['list']:
                                    if not (nn['isnew'] in '2'):
                                        list_str += '{"di":' + nn['t1'] + ',"tm":"' + nn['ts'] + '","title":"' + nn[
                                            't2'] + '","url":"https://www.mgtv.com'
                                        list_str += nn['url'] + '","img":"' + nn['img'] + '"},'
                            list_str = list_str[:-1] + ']'
                            anime.update(animeurl=list_str,animecount=count)
                        except KeyError as e:
                            anime.update(animeurl='[]',animecount=count)
                        print('更新视频信息.......................................................')
                        print(info)
                    else:
                        print('已经添加本条信息!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        print(info)
                info.clear()
    driver.close()

def mgtv(temp):
    print(temp)
    print('????????????????????????????????????????????????????????????')
    if '电影' in temp:
        mgtvmovies()
    elif '电视剧' in temp:
        mgtvtv()
    elif  '动漫' in temp:
        mgtvanime()
    elif  '纪录片' in temp:
        mgtvdocumentary()
    else:
        return 0
