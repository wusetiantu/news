# -*- coding:utf-8 -*-
"""
@author:Levy
@file:bloomberg.py
@time:17-8-3上午10:41
"""
import requests
from lxml import etree
from dateutil import parser as dp
from pyquery import PyQuery as pq
from datetime import datetime
import pymongo
import json

first_header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'www.bbc.co.uk',
    'Referer':'http://www.bbc.co.uk/search?q=bitcoin',
    'X-Requested-With':'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
}
def donwnload(url,Header=None):
    if Header:
        r = requests.get(url=url,headers=Header)
    else:
        r = requests.get(url=url)
    try:
        html = r.content
    except:
        html = None
    return html
def start(START_URL,DB):
    html_str = donwnload(url = START_URL, Header = first_header)
    doc = pq(html_str)
    articles = doc('article')
    for each in articles.items():
        twoq = pq(each.html())
        href = twoq('h1 > a ').attr['href']
        if href.find('technology')!=-1:
            y_dic = {'url':href}
            num_true = DB['news'].find(y_dic).count()
            if num_true: pass
            else:
                news_str = twoq('time').attr['datetime']
                title = twoq('h1 > a').text()
                instroduction = twoq('.long').text()
                news_time = dp.parse(news_str)
                second_html = donwnload(url=href)
                content = getcontent(html=second_html)
                r_dic = {
                    'time':news_time,
                    'title':title,
                    'content_html':second_html.decode('utf-8'),
                    'url':href,
                    'content':content,
                    'web':'bbc.com',
                    'newsfrom':'bbc.com',
                    'spider_time':datetime.now(),
                    '_type':'news',
                    'instroduction': instroduction
                }
                try:
                    DB['news'].insert(r_dic)
                except:
                    pass

def getcontent(html):
    doc = pq(html)
    div = doc('.story-body__inner > p')
    content = ''
    for each in div.items():
        content += each.text() + '\n'
    return content

if __name__=="__main__":
    start_url = "http://www.bbc.co.uk/search/more?page=1&q=bitcoin"

    conn = pymongo.MongoClient(host='localhost',port=27017)
    db = conn['sina']
    start(START_URL=start_url,DB=db)








































