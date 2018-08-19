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
from ..models import Movies,Tvseries,Anime,Documentary

def youkumovies():
    flag = 0
    boo = False
    countsum = 0
    lg = {'内地': '普通话', '韩国': '韩语', '美国': '英语', '俄罗斯': '俄语', '比利时': '比利时语',
      '香港': '粤语', '台湾': '台语', '日本': '日语', '其他': '其他', '泰国': '泰语',
      '欧洲': '英语', '印度': '印度语', '英国': '英语', '中国': '普通话'}
    url = 'http://list.youku.com/category/show/c_96_s_6_d_1_p_%d.html?spm=a2h1n.8251845.0.0'
    for ii in range(0,29):
        flag += 1
        sum = 0
        print('..........................正在添加第%d页的信息.........................' %(flag))
        page = url %(ii)
        req = requests.get(page)
        soup = BeautifulSoup(req.text, 'lxml')
        html = soup.find_all(class_='yk-col4 mr1')
        for n in html:
            sum += 1
            countsum += 1
            print('>>>>>>>>>>>>>>>>>>>>>>>当前总共提取了 %d 条信息<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<' % (countsum))
            print('---------------------正在添加第 %d 页的第 %d 条信息------------------------' % (flag, sum))
            if countsum >= 685:
                new_str = str(n)
                new_str = BeautifulSoup(new_str, 'lxml')
                html_str = str(new_str.find_all(class_='p-thumb')[0])
                # print(html_str)
                try:
                    info = re.findall('class="p-thumb"><a href="(.*?)" target="_blank"', html_str, re.S)
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('target="_blank" title="(.*?)"></a>', html_str, re.S)[0].replace('\xa0', ''))
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('</div><img _src="(.*?)" alt="', html_str, re.S)[0])
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('<span class="vip-free">(.*?)</span>', html_str, re.S)[0])
                except IndexError as e:
                    info.append('')
                if not ('预告' in info[3]):
                    if(len(Movies.objects.filter(moviesname=info[1]))<1):
                        dan_req = requests.get('http:' + info[0])
                        new_html = dan_req.text.replace('\\n', '').replace('\n', '').replace('\\', '')
                        try:
                            dan_url = 'https:' + re.findall('class="bg-dubo"></span>    <a href="(.*?)" target="_blank"', new_html, re.S)[0]
                        except IndexError as e:
                            dan_url = 'https://www.baidu.com'
                        req = requests.get(dan_url)
                        y_html = BeautifulSoup(req.text, 'lxml')
                        try:
                            html_s = str(y_html.find_all(class_='p-base')[0])
                            tv_time = re.findall('<label>上映：</label>(.*?)</span></li>', html_s, re.S)[0]
                            info.append(tv_time)
                        except IndexError as e:
                            info.append('')
                            html_s = ''
                        try:
                            tv_di = re.findall('</li><li>地区：.*target="_blank">(.*?)</a></li><li>类型：', html_s, re.S)[0]
                            info.append(tv_di)
                        except IndexError as e:
                            info.append('')
                            tv_di = '其他'
                        try:
                            info.append(lg[tv_di])
                        except KeyError as e:
                            info.append('')
                        try:
                            lei_s = re.findall('</a></li><li>类型：<a(.*?)</li><li>', html_s, re.S)[0]
                            dan_lei = re.findall('target="_blank">(.*?)</a>', lei_s, re.S)
                            z_lei = ''
                            for aa in dan_lei:
                                z_lei += aa
                            info.append(z_lei)
                        except IndexError as e:
                            info.append('')
                        if info[2] != '':
                            movies = Movies(moviesname=info[1],moviessource='优酷视频',
                            moviesgrade=info[3],movieslanguage=info[6],
                            moviestype=info[7],moviesdecade=info[4],moviesregion=info[5],
                            pdatetime=info[4],moviesimageurl=info[2],moviesurl='https:'+info[0],moviesurl2='[]')
                            movies.save()
                            print('成功的添加一条信息+++++++++++++++++++++++++++++++++++++++++++++++++++')
                        else:
                            print('数据失败.............................................................')
                        # print(info[:10])
                    elif len(Movies.objects.filter(moviesname=info[1])) >= 1:
                        print('已经添加本条信息!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        print(info)
                    else:
                        print('已经添加本条信息!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        print(info)
                info.clear()

def youku(temp):
    print(temp)
    print('????????????????????????????????????????????????????????????')
    if '电影' in temp:
        youkumovies()
    elif '电视剧' in temp:
        youkutv()
    elif  '动漫' in temp:
        youkuanime()
    elif  '纪录片' in temp:
        youkudocumentary()
    else:
        return 0
