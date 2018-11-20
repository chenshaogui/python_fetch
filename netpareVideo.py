import threading
from bs4 import BeautifulSoup
import os
import requests
import re
import pymongo
import time
import random


myclient = pymongo.MongoClient('mongodb://localhost:27017/');
dblist=myclient.list_database_names();
#创建数据库，没有插入数据不会创建成功
db = myclient['video'];
collection=db['nets_video'];

domain="http://99f2d.com"
#请求数据
def get_response(url):
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response=requests.get(url=url,headers=headers).content
    return response

#返回网页数据，找到对应的格式
def get_content(html):
    videoObj=[]
    soup=BeautifulSoup(html,"html.parser")
    #print(soup.prettify())
    videoClass=[];
    list=soup.select("ol li a")
    for i in range(1,len(list)):
        videoClass.append(domain+list[i].get("href"))
    for item in videoClass:
        htmldom=get_response(item)
        soup=BeautifulSoup(htmldom,'html.parser')
        pageItem=soup.select(".nextPage a")
        domurl=pageItem[0].get("href")
        pageurl=domain+domurl;
        pageurl=pageurl[:-1]
        pagesize=pageItem[len(pageItem)-2].string
        for i in range(1,int(pagesize)+1):
            #sleep_time = random.randint(1, 3)
            #time.sleep(sleep_time)
            newpageurl=pageurl+str(i)
            videoObj.append(newpageurl)
            htmldom2=get_response(newpageurl)
            soup2=BeautifulSoup(htmldom2,"html.parser")
            list2 = soup2.select('.detail_right_div ul a')
            for val in list2:
                fallUrl=val.get('href')
                fallUrl=domain+fallUrl
                htmldom3=get_response(fallUrl)
                soup3=BeautifulSoup(htmldom3,"html.parser")
                list3=soup3.select('script')[6].string
                list4=soup3.title.string
                #r = r"url = '(http.*\.m3u8)'"
                #r1=r"picurl = '(http.*\.jpg)'"
                #r2=r"(.*\.)"
                r = r"(http.*\.m3u8)"
                r1 = r"(http.*\.jpg)"
                r2 = r"(.*\.)"
                re_video=re.compile(r)
                re_img=re.compile(r1)
                re_name=re.compile(r2)
                #videoUrl=re.findall(re_video,list3)
                #img=re.findall(re_img,list3)
                #name=re.findall(re_name,list4)
                match1=re.search(re_video,list3)
                if  match1:
                    videoUrl=match1.group(0)
                match2=re.search(re_img,list3)
                if  match2:
                    img=match2.group(0)
                match3=re.search(re_name,list4)
                if match3:
                    name=match3.group(0)
                record = {'videoUrl': videoUrl, 'name': name,
                      'img': img}
                collection.insert_one(record)
                print(videoUrl)
                print(img)
                print(name)


def findUrl(obj):
    useURl=[]
    for item in obj:
        soup=BeautifulSoup(item,"html.parser")
        list=soup.select(".detail_right_div ul li")
        for index in list:
            openUrl=index.select("a")[0].get("href")
            newUrl=domain+openUrl
            print(newUrl)
            useURl.append(newUrl)

#主函数入口
if __name__ == '__main__':
    urlStr='http://99f2d.com/video'
    html=get_response(urlStr)
    videoObj=get_content(html)
    #findUrl(videoObj)