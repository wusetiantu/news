# -*- coding:utf-8 -*-
import requests
from lxml import etree
from dateutil import parser as dp
from pyquery import PyQuery as pq
from datetime import datetime
import pymongo
import json

first_header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'widgets.bitcoin.com',
    'Upgrade-Insecure-Requests': '1',
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
    json_str = donwnload(url = START_URL, Header = first_header)
    if json_str:
        list1 = json.loads(json_str)
        for dic_lis in list1:
            href = dic_lis['url']
            y_dic = {'url':href}
            print(y_dic)
            num_ture = DB['news'].find(y_dic).count()
            if num_ture:
                pass
            else:
                news_time_str = dic_lis['stamp']
                news_time_str = news_time_str.replace('+0000','')
                news_time_strs = news_time_str.split(',')
                news_time = datetime.strptime(news_time_strs[1].strip(),'%d %b %Y %H:%M:%S')
                title = dic_lis['title']
                second_html = donwnload(url=href)
                content = getcontent(html=second_html)
                instroduction = dic_lis['text']
                print(second_html.decode('utf-8'))
                r_dic = {
                    'time':news_time,
                    'title':title,
                    'content_html':second_html.decode('utf-8'),
                    'url':href,
                    'content':content,
                    'web':'news.bitcoin.com',
                    'newsfrom':'news.bitcoin.com',
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
    div = doc('.td-post-content > p')
    content = ''
    for each in div.items():
        if content.find('Images')!=-1:
            break
        else:
            content += each.text() + '\n'
    return content

if __name__=="__main__":
    start_url = "https://widgets.bitcoin.com/news.json"
    conn = pymongo.MongoClient(host='localhost',port=27017)
    db = conn['sina']
    start(START_URL=start_url,DB=db)
# import json
# obj = [[1,2,3],123,123.123,'abc',{'key1':(1,2,3),'key2':(4,5,6)}]
# encodejson = json.dumps(obj)

# print(obj)
# print(type(obj))
# print(encodejson)
#
# print(type(encodejson))

# decode = json.loads(encodejson)
# print(type(decode))








































