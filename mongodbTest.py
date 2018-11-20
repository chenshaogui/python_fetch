import pymongo;
import os;
import sys;
import time;
import linecache;
import os.path;
import datetime


myclient = pymongo.MongoClient('mongodb://localhost:27017/');
dblist=myclient.list_database_names();
#创建数据库，没有插入数据不会创建成功
db = myclient['video'];
collection=db['ower_video'];

#时间差5分钟执行一次
subtime=300
# dic={'name':'张三','id':'123','age':'45'}
# collection.insert_one(dic)
# list_of_records = [{'name': 'amy', 'id': 1798},{'name': 'bob', 'id': 1631}]
# collection.insert_many(list_of_records)


#查询一条
# collection.find_one({'name':'amy'})
#
#
# for record in collection.find_one({'name':'amy'}):
#     print(record)
#
# for record in collection.find({'name':'amy'}):
#     print(record)
#
# print(collection.count())
#
# if 'test2' in dblist:
#     print('数据库存在')

#取D盘主目录
#PATH='D:'
# list_dir=os.listdir(PATH)
# for li in list_dir:
#     print(li)

#name=os.path.splitext('E:\Youxun\1504776873262.jpg')
#print(name[1])

# for(path,dirs,files) in os.walk('F:\\'):
#     for filename in files:
#         impl=path+'\\'+filename
#         name=os.path.splitext(impl)[1]
#         if(name=='.mp4'):
#             print(impl)


# listPath=os.listdir('F:\\')
# for i in range(0,len(listPath)):
#     paths=os.path.join("F:\\",listPath[i])
#     print(paths)
path='F:\\'
imagePath='M:\OwerVideo\Images\\'

def inser_video_mongodb(path):
    for (root, dirs, files) in os.walk("M:\\OwerVideo"):
        for filename in files:
            videoUrl=os.path.join(root,filename)
            type=os.path.splitext(videoUrl)[1]
            filedir=os.path.splitext(videoUrl)[0]
            name=os.path.splitext(filename)[0]
            size=os.path.getsize(videoUrl)/1024/1024
            timestamp=int(time.time())
            if(type=='.avi' or type=='.mp4' or type=='.3gp' or type=='.rmvb' or type=='.mkv' or type=='.wmv' or type=='.flv' or type=='.mov'):
                str_video = "ffmpeg -ss 0:5:00 -i " + videoUrl + " " + "-vframes 1 -y -f image2 " + imagePath+name+str(timestamp)+ ".jpg"
                print(str_video)
                image = os.popen(str_video)
                imagedir=imagePath +name+str(timestamp)+'.jpg'
                #print(str_video)
                #print(videoUrl)
                #print(imagedir)
                record={'videoUrl':videoUrl,'name':name,'size':int(size),'type':type,'timestamp':timestamp,'img':imagedir}
                collection.insert_one(record)
                #print(image)



def creat_video_image(path):
    for (root,dirs,files) in os.walk(path):
        for filename in files:
            video_path=os.path.join(root,filename)
            filetime=os.path.getmtime(video_path)
            localtime=time.time();
            tx=localtime-filename;
            if tx<subtime:
                str_md5='md5sum'+video_path+' '+"| awk  '{print $1}'"
                video_md5=os.popen(str_md5).readline(32)
                str_video="ffmpeg -ss 0:1:00 -i "+" "+video_path+" "+"-r 0.01 -f image2 "+filename+".jpeg"
                image=os.popen(str_video)



    # for dirc in dirs:
    #     print(os.path.join(root,dirc))

if __name__ == "__main__":
    inser_video_mongodb(path)