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

def txmovies():
    flag = 0
    count = 0
    driver = webdriver.Chrome()
    driver.set_window_size(1080, 920)
    url = 'https://v.qq.com/x/list/movie?sort=19&offset=%d'
    lg = {'内地': '普通话', '韩国': '韩语', '美国': '英语', '俄罗斯': '俄语', '比利时': '比利时语',
      '香港': '粤语', '台湾': '台语', '日本': '日语', '其他': '其他', '泰国': '泰语', '欧美': '英语', '印度': '印度语'}
    for i in range(0,166):
        flag += 1
        sum = 0
        print('..........................正在添加第%d页的信息.........................' %(flag))
        page = url %(i*30)
        req = requests.get(page)
        soup = BeautifulSoup(req.text, 'lxml')
        html = soup.find_all(class_='list_item')
        for n in html:
            sum += 1
            count += 1
            print('>>>>>>>>>>>>>>>>>>>>>>>当前总共提取了 %d 条信息<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<' % (count))
            print('---------------------正在添加第 %d 页的第 %d 条信息------------------------' % (flag, sum))
            html_str = str(n)
            try:
                info = re.findall('<a _stat2="videos:pic" class="figure" data-float=".*" href="(.*?)" tabindex="', html_str, re.S)
            except IndexError as e:
                info.append('')
            try:
                info.append(re.findall('[^mark_v">]<img alt="(.*?)" r-imgerr="v"', html_str, re.S)[0].replace('\xa0', ''))
            except IndexError as e:
                info.append('')
            try:
                info.append(re.findall('r-imgerr="v" r-lazyload="(.*?)" src="', html_str, re.S)[0])
            except IndexError as e:
                info.append('')
            try:
                info.append(re.findall('<i class="mark_v"><img alt="(.*?)" src="', html_str, re.S)[0])
            except IndexError as e:
                info.append('')
            try:
                pf = re.findall('<em class="score_l">(.*?)</em>', html_str, re.S)[0]
                pf += re.findall('<em class="score_s">(.*?)</em>', html_str, re.S)[0]
                info.append(float(str(pf)))
            except IndexError as e:
                info.append(0.0)
            if not ('期' in info[3]):
                if(len(Movies.objects.filter(moviesname=info[1]))<1):
                    driver.get(info[0])
                    new_html = driver.page_source
                    lei = re.findall('target="_blank" class="tag_item">(.*?)</a>', new_html, re.S)
                    try:
                        info.append(lei[0])
                    except IndexError as e:
                        info.append('')
                    try:
                        info.append(lei[1])
                    except IndexError as e:
                        info.append('')
                    try:
                        try:
                            info.append(lg[lei[0]])
                        except IndexError as e:
                            info.append('')
                    except KeyError as e:
                        info.append('')
                    try:
                        ss = ''
                        for k in lei[2:]:
                            ss += k
                        info.append(ss)
                    except IndexError as e:
                        info.append('')
                    movies = Movies(moviesname=info[1],moviessource='腾讯视频',
                    moviesgrade=info[3],movieslanguage=info[7],moviestype=info[8],
                    moviesdecade=info[6],moviesregion=info[5],pdatetime=info[6],moviesimageurl=info[2],
                    moviesurl=info[0],moviesurl2='[]')
                    movies.save()
                    print('++++++++++++++++成功的添加一条信息',info)
                else:
                    print('已经添加本条信息!!!!!',info)
            else:
                print('已经添加本条信息>>>>>',info)
            info.clear()
    driver.close()

def txtv():
    flag = 0
    boo = False
    countsum = 0
    url = 'http://v.qq.com/x/list/tv?feature=-1&sort=19&ipay=-1&iarea=-1&iyear=-1&offset=%d'
    for ii in range(0,119):
        flag += 1
        sum = 0
        print('..........................正在添加第%d页的信息.........................' %(flag))
        page = url %(ii*30)
        req = requests.get(page)
        soup = BeautifulSoup(req.text, 'lxml')
        html = soup.find_all(class_='list_item')
        for n in html:
            sum += 1
            countsum += 1
            print('>>>>>>>>>>>>>>>>>>>>>>>当前总共提取了 %d 条信息<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<' % (countsum))
            print('---------------------正在添加第 %d 页的第 %d 条信息------------------------' % (flag, sum))
            if countsum >= 1:
                html_str = str(n)
                try:
                    info = re.findall('<a _stat2="videos:pic" class="figure" data-float=".*" href="(.*?)" tabindex="', html_str, re.S)
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('[^mark_v">]<img alt="(.*?)" r-imgerr="v"', html_str, re.S)[0].replace('\xa0', ''))
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('r-imgerr="v" r-lazyload="(.*?)" src="', html_str, re.S)[0])
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('<i class="mark_v"><img alt="(.*?)" src="', html_str, re.S)[0])
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('figure_info">\D*(\d+)集</span>', html_str, re.S)[0])
                except IndexError as e:
                    info.append('')
                if not ('预告' in info[3]):
                    count = 0
                    try:
                        count = int(info[4])
                    except ValueError as e:
                        count = 0
                    tv = Tvseries.objects.filter(tvname=info[1])
                    if(len(tv)<1 and count > 0):
                        try:
                            dan_url = re.findall('https://v.qq.com/x/cover/(.*)', info[0], re.S)[0]
                        except IndexError as e:
                            dan_url = ''
                        dan_req = requests.get('https://v.qq.com/detail/h/' + dan_url)
                        dan_soup = BeautifulSoup(dan_req.text, 'lxml')
                        try:
                            new_html = str(dan_soup.find_all(class_='mod_episode')[0]).replace('\n', '')
                        except IndexError as e:
                            new_html = ''
                        tv_url = re.findall('href="(.*?)" itemprop="url"', new_html, re.S)
                        if len(tv_url) < 1:
                            tv_url = re.findall('href="(.*?)" target="_blank"', new_html, re.S)
                        if len(tv_url) < 1:
                            tv_url = re.findall('href="(.*?)" target="_blank" itemprop="url"', new_html, re.S)
                        try:
                            di_html = str(dan_soup.find_all(class_='video_type cf')[0]).replace('\n', '')
                        except IndexError as e:
                            di_html = ''
                        try:
                            tv_di = re.findall('地　区:</span><span class="type_txt">(.*?)</span>', di_html, re.S)[0]
                        except IndexError as e:
                            tv_di = ''
                        try:
                            tv_lag = re.findall('语　言:</span><span class="type_txt">(.*?)</span>', di_html, re.S)[0]
                        except IndexError as e:
                            tv_lag = ''
                        info.append(tv_di)
                        info.append(tv_lag)
                        try:
                            time_html = str(dan_soup.find_all(class_='video_type video_type_even cf')[0]).replace('\n', '')
                        except IndexError as e:
                            time_html = ''
                        try:
                            tv_time = re.findall('出品时间:</span><span class="type_txt">(.*?)</span>', time_html, re.S)[0]
                        except IndexError as e:
                            tv_time = ''
                        info.append(tv_time)
                        try:
                            lei_html = str(dan_soup.find_all(class_='tag_list')[0]).replace('\n', '')
                        except IndexError as e:
                            lei_html = ''
                        try:
                            tv_lei = re.findall('target="_blank">(.*?)</a>', lei_html, re.S)
                        except IndexError as e:
                            tv_lei = ''
                        str_lei = ''
                        for mm in tv_lei:
                            str_lei += mm
                        info.append(str_lei)
                        print(tv_url)
                        list_str = '['
                        if len(tv_url) > 0:
                            for i in range(1, len(tv_url)+1):
                                if i <= count:
                                    list_str += '{"di":"' + str(i) + '","url":"' + tv_url[i-1] + '"},'
                        list_str = list_str[:-1] + ']'
                        info.append(list_str)
                        tvseries = Tvseries(tvname=info[1],tvource='腾讯视频',
                        tvcount=count,tvgrade=info[3],tvlanguage=info[6],
                        tvtype=info[8],tvdecade=info[7],tvregion=info[5],
                        pdate=info[7],tvimageurl=info[2],tvurl=info[9],tvurl2='[]')
                        tvseries.save()
                        print('成功的添加一条信息+++++++++++++++++++++++++++++++++++++++++++++++++++')
                        # print(info[:10])
                    elif len(tv) >= 1:
                        if tv[0].tvcount < count and count > 0:
                            try:
                                dan_url = re.findall('https://v.qq.com/x/cover/(.*)', info[0], re.S)[0]
                            except IndexError as e:
                                dan_url = ''
                            dan_req = requests.get('https://v.qq.com/detail/h/' + dan_url)
                            dan_soup = BeautifulSoup(dan_req.text, 'lxml')
                            try:
                                new_html = str(dan_soup.find_all(class_='mod_episode')[0]).replace('\n', '')
                            except IndexError as e:
                                new_html = ''
                            tv_url = re.findall('<a href="(.*?)" itemprop="url"', new_html, re.S)
                            if len(tv_url) < 1:
                                tv_url = re.findall('href="(.*?)" target="_blank"', new_html, re.S)
                            if len(tv_url) < 1:
                                tv_url = re.findall('href="(.*?)" target="_blank" itemprop="url"', new_html, re.S)
                            list_str = '['
                            if len(tv_url) > 0:
                                for i in range(1, count+1):
                                    list_str += '{"di":"' + str(i) + '","url":"' + tv_url[i-1] + '"},'
                            list_str = list_str[:-1] + ']'
                            tv.update(tvurl=list_str,tvcount=count)
                            print('更新视频信息.......................................................')
                            print(info)
                    else:
                        print('已经添加本条信息!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        print(info)
                info.clear()

def txanime():
    flag = 0
    boo = False
    countsum = 0
    lg = {'内地': '普通话', '韩国': '韩语', '美国': '英语', '俄罗斯': '俄语', '比利时': '比利时语',
      '香港': '粤语', '台湾': '台语', '日本': '日语', '其他': '其他', '泰国': '泰语', '欧美': '英语', '印度': '印度语'}
    url = 'http://v.qq.com/x/list/cartoon?itype=-1&ipay=-1&iarea=-1&language=-1&sort=19&iyear=-1&plot_aspect=-1&offset=%d'
    for ii in range(0,80):
        flag += 1
        sum = 0
        print('..........................正在添加第%d页的信息.........................' %(flag))
        page = url %(ii*30)
        req = requests.get(page)
        soup = BeautifulSoup(req.text, 'lxml')
        html = soup.find_all(class_='list_item')
        for n in html:
            sum += 1
            countsum += 1
            print('>>>>>>>>>>>>>>>>>>>>>>>当前总共提取了 %d 条信息<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<' % (countsum))
            print('---------------------正在添加第 %d 页的第 %d 条信息------------------------' % (flag, sum))
            if countsum >= 1:
                html_str = str(n)
                try:
                    info = re.findall('<a _stat2="videos:pic" class="figure" data-float=".*" href="(.*?)" tabindex="', html_str, re.S)
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('[^mark_v">]<img alt="(.*?)" r-imgerr="v"', html_str, re.S)[0].replace('\xa0', ''))
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('r-imgerr="v" r-lazyload="(.*?)" src="', html_str, re.S)[0])
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('<i class="mark_v"><img alt="(.*?)" src="', html_str, re.S)[0])
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('figure_info">\D*(\d+)集</span>', html_str, re.S)[0])
                except IndexError as e:
                    info.append('')
                if not ('预告' in info[3]):
                    count = 0
                    try:
                        count = int(info[4])
                    except ValueError as e:
                        count = 0
                    anime = Anime.objects.filter(animename=info[1])
                    if(len(anime)<1 and count > 0):
                        try:
                            dan_url = re.findall('https://v.qq.com/x/cover/(.*)', info[0], re.S)[0]
                        except IndexError as e:
                            dan_url = ''
                        dan_req = requests.get('https://v.qq.com/detail/h/' + dan_url)
                        dan_soup = BeautifulSoup(dan_req.text, 'lxml')
                        try:
                            new_html = str(dan_soup.find_all(class_='mod_episode')[0]).replace('\n', '')
                        except IndexError as e:
                            new_html = ''
                        print('new_html',new_html)
                        tv_url = re.findall('href="(.*?)" itemprop="url"', new_html, re.S)
                        if len(tv_url) < 1:
                            tv_url = re.findall('href="(.*?)" target="_blank"', new_html, re.S)
                        if len(tv_url) < 1:
                            tv_url = re.findall('href="(.*?)" target="_blank" itemprop="url"', new_html, re.S)
                        try:
                            di_html = str(dan_soup.find_all(class_='video_type cf')[0]).replace('\n', '')
                        except IndexError as e:
                            di_html = ''
                        try:
                            tv_di = re.findall('地　区:</span><span class="type_txt">(.*?)</span>', di_html, re.S)[0]
                        except IndexError as e:
                            tv_di = ''
                        info.append(tv_di)
                        try:
                            info.append(lg[tv_di])
                        except KeyError as e:
                            info.append('其他')
                        try:
                            tv_time = re.findall('出品时间:</span><span class="type_txt">(.*?)</span>', di_html, re.S)[0]
                        except IndexError as e:
                            tv_time = ''
                        info.append(tv_time)
                        try:
                            lei_html = str(dan_soup.find_all(class_='tag_list')[0]).replace('\n', '')
                        except IndexError as e:
                            lei_html = ''
                        try:
                            tv_lei = re.findall('target="_blank">(.*?)</a>', lei_html, re.S)
                        except IndexError as e:
                            tv_lei = ''
                        str_lei = ''
                        for mm in tv_lei:
                            str_lei += mm
                        info.append(str_lei)
                        print(tv_url)
                        list_str = '['
                        if len(tv_url) > 0:
                            for i in range(1, len(tv_url)+1):
                                if i <= count:
                                    list_str += '{"di":"' + str(i) + '","url":"' + tv_url[i-1] + '"},'
                        list_str = list_str[:-1] + ']'
                        info.append(list_str)
                        ani = Anime(animename=info[1],animeource='腾讯视频',
                        animecount=count,animegrade=info[3],animelanguage=info[6],
                        animetype=info[8],animedecade=info[7],animeregion=info[5],
                        pdate=info[7],animeimageurl=info[2],animeurl=info[9],animeurl2='[]')
                        ani.save()
                        print('成功的添加一条信息+++++++++++++++++++++++++++++++++++++++++++++++++++')
                        # print(info[:10])
                    elif len(anime) >= 1:
                        if anime[0].animecount < count and count > 0:
                            try:
                                dan_url = re.findall('https://v.qq.com/x/cover/(.*)', info[0], re.S)[0]
                            except IndexError as e:
                                dan_url = ''
                            dan_req = requests.get('https://v.qq.com/detail/h/' + dan_url)
                            dan_soup = BeautifulSoup(dan_req.text, 'lxml')
                            try:
                                new_html = str(dan_soup.find_all(class_='mod_episode')[0]).replace('\n', '')
                            except IndexError as e:
                                new_html = ''
                            tv_url = re.findall('<a href="(.*?)" itemprop="url"', new_html, re.S)
                            if len(tv_url) < 1:
                                tv_url = re.findall('<a href="(.*?)" target="_blank"', new_html, re.S)
                            if len(tv_url) < 1:
                                tv_url = re.findall('<a href="(.*?)" target="_blank" itemprop="url"', new_html, re.S)
                            list_str = '['
                            if len(tv_url) > 0:
                                for i in range(1, count+1):
                                    list_str += '{"di":"' + str(i) + '","url":"' + tv_url[i-1] + '"},'
                            list_str = list_str[:-1] + ']'
                            anime.update(animeurl=list_str,animecount=count)
                            print('更新视频信息.......................................................')
                            print(info)
                    else:
                        print('已经添加本条信息!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        print(info)
                info.clear()
def txdocumentary():
    flag = 0
    boo = False
    countsum = 0
    lg = {'内地': '普通话', '韩国': '韩语', '美国': '英语', '俄罗斯': '俄语', '比利时': '比利时语',
      '香港': '粤语', '台湾': '台语', '日本': '日语', '其他': '其他', '泰国': '泰语',
      '欧洲': '英语', '印度': '印度语', '英国': '英语'}
    url = 'http://v.qq.com/x/list/doco?sort=19&ipay=-1&itrailer=-1&itype=-1&offset=%d'
    for ii in range(0,118):
        flag += 1
        sum = 0
        print('..........................正在添加第%d页的信息.........................' %(flag))
        page = url %(ii*30)
        req = requests.get(page)
        soup = BeautifulSoup(req.text, 'lxml')
        html = soup.find_all(class_='list_item')
        for n in html:
            sum += 1
            countsum += 1
            print('>>>>>>>>>>>>>>>>>>>>>>>当前总共提取了 %d 条信息<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<' % (countsum))
            print('---------------------正在添加第 %d 页的第 %d 条信息------------------------' % (flag, sum))
            if countsum >= 1:
                html_str = str(n)
                try:
                    info = re.findall('<a _stat2="videos:pic" class="figure" data-float=".* href="(.*?)" tabindex="-1"', html_str, re.S)
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('[^mark_v">]<img alt="(.*?)" r-imgerr="v"', html_str, re.S)[0].replace('\xa0', ''))
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('r-imgerr="v" r-lazyload="(.*?)" src="', html_str, re.S)[0])
                except IndexError as e:
                    info.append('')
                try:
                    info.append(re.findall('<i class="mark_v"><img alt="(.*?)" src="', html_str, re.S)[0])
                except IndexError as e:
                    info.append('')
                if not ('预告' in info[3]):
                    documentary = Documentary.objects.filter(documentaryname=info[1])
                    if(len(documentary)<1):
                        dan_url = re.findall('https://v.qq.com/x/cover/(.*)', info[0], re.S)[0]
                        dan_req = requests.get('https://v.qq.com/detail/h/' + dan_url)
                        dan_soup = BeautifulSoup(dan_req.text, 'lxml')
                        try:
                            new_html = str(dan_soup.find_all(class_='mod_episode')[0]).replace('\n', '')
                            tv_url = re.findall('href="(.*?)" itemprop="url"', new_html, re.S)
                            if len(tv_url) < 1:
                                tv_url = re.findall('href="(.*?)" target="_blank"', new_html, re.S)
                            if len(tv_url) < 1:
                                tv_url = re.findall('href="(.*?)" target="_blank" itemprop="url"', new_html, re.S)
                        except IndexError as e:
                            tv_url = []
                        try:
                            di_html = str(dan_soup.find_all(class_='video_type cf')[0]).replace('\n', '')
                            tv_di = re.findall('地　区:</span><span class="type_txt">(.*?)</span>', di_html, re.S)
                            tv_time = re.findall('播出时间:</span><span class="type_txt">(.*?)</span>', di_html, re.S)
                            info.append(tv_di[0])
                        except IndexError as e:
                            info.append('其他')
                        try:
                            try:
                                info.append(lg[tv_di[0]])
                            except IndexError as e:
                                info.append('其他')
                        except KeyError as e:
                            info.append('其他')
                        try:
                            info.append(tv_time[0])
                        except IndexError as e:
                            info.append('2018-01-01')
                        try:
                            lei_html = str(dan_soup.find_all(class_='tag_list')[0]).replace('\n', '')
                            tv_lei = re.findall('target="_blank">(.*?)</a>', lei_html, re.S)
                            lei_str = ''
                            for aa in tv_lei:
                                lei_str += aa
                            info.append(lei_str)
                        except IndexError as e:
                            info.append('其他')
                        list_str = '['
                        if len(tv_url) > 0:
                            for i in range(0, len(tv_url)):
                                list_str += '{"di":"' + str(i+1) + '","url":"' + tv_url[i] + '"},'
                        list_str = list_str[:-1] + ']'
                        info.append(list_str)
                        doc = Documentary(documentaryname=info[1],documentarysource='腾讯视频',
                        documentarycount=len(tv_url),documentarygrade=info[3],documentarylanguage=info[5],
                        documentarytype=info[7],documentarydecade=info[6],documentaryregion=info[4],
                        pdatetime=info[6],documentaryimageurl=info[2],documentaryurl=info[8],documentaryurl2='[]')
                        doc.save()
                        print('成功的添加一条信息+++++++++++++++++++++++',info[:7])
                        # print(info[:10])
                    elif len(documentary) >= 1:
                        dan_url = re.findall('https://v.qq.com/x/cover/(.*)', info[0], re.S)[0]
                        dan_req = requests.get('https://v.qq.com/detail/h/' + dan_url)
                        dan_soup = BeautifulSoup(dan_req.text, 'lxml')
                        try:
                            new_html = str(dan_soup.find_all(class_='mod_episode')[0]).replace('\n', '')
                            tv_url = re.findall('href="(.*?)" itemprop="url"', new_html, re.S)
                        except IndexError as e:
                            tv_url = []
                        if len(tv_url) < 1:
                            tv_url = re.findall('href="(.*?)" target="_blank"', new_html, re.S)
                        if len(tv_url) < 1:
                            tv_url = re.findall('href="(.*?)" target="_blank" itemprop="url"', new_html, re.S)
                        if documentary[0].documentarycount < len(tv_url) and len(tv_url) > 0:
                            list_str = '['
                            if len(tv_url) > 0:
                                for i in range(0, len(tv_url)):
                                    list_str += '{"di":"' + str(i+1) + '","url":"' + tv_url[i] + '"},'
                            list_str = list_str[:-1] + ']'
                            documentary.update(documentaryurl=list_str,documentarycount=len(tv_url))
                            print('更新视频信息.......................................................')
                            print(info)
                    else:
                        print('已经添加本条信息!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        print(info)
                info.clear()

def tx(temp):
    print(temp)
    print('????????????????????????????????????????????????????????????')
    if '电影' in temp:
        txmovies()
    elif '电视剧' in temp:
        txtv()
    elif  '动漫' in temp:
        txanime()
    elif  '纪录片' in temp:
        txdocumentary()
    else:
        return 0
