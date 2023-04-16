import pymongo, os, json, datetime, random
from bson import ObjectId

ip = '127.0.0.1'
port = 27017
database = 'workorder'
# 请注意，启动程序之前必须配置ip,port和database，否则连接不上数据库会报错

client = pymongo.MongoClient("mongodb+srv://HeyCrab3:gangcheng114514>>.@holyshit.cdcxwyp.mongodb.net/?retryWrites=true&w=majority")
db = None


def get_db():
    global db
    if not db:
        db = client[database]
    return db


db = get_db()

data_path = './data'

def data_import():
    coll_list = db.list_collection_names()
    for collection in coll_list:
        # 删除集合
        db[collection].drop()
    for maindir, subdir, file_list in os.walk(data_path):
        for file_name in file_list:
            if file_name[file_name.rindex('.'):] == '.json':
                coll = file_name[:file_name.rindex('.')]

                with open(data_path + '/' + file_name, encoding='utf-8') as file:
                    str = file.read()
                    if str == '' or str is None:
                        continue
                    else:
                        data = []
                        data.extend(json.loads(str))
                        if coll == 'user':
                            for d in data:
                                d['_id'] = ObjectId(d['_id'])
                                d['userName'] = d['userName']
                                d['passWord'] = d['passWord']
                                d['perm'] = d['perm']
                        if coll == 'workorder':
                            for d in data:
                                d['_id'] = ObjectId(d['_id'])
                                d['title'] = d['title']
                                d['sender'] = d['sender']
                                d['senderID'] = ObjectId(d['senderID'])
                                d['content'] = d['content']
                                d['status'] = d['status']
                                d['time'] = d['time']
                        if coll == 'wiki':
                            for d in data:
                                d['_id'] = ObjectId(d['_id'])
                                d['title'] = d['title']
                                d['child'] = d['child']
                        if coll == 'reply':
                            for d in data:
                                d['_id'] = ObjectId(d['_id'])
                                d['replyTo'] = d['replyTo']
                                d['content'] = d['content']
                                d['sender'] = d['sender']
                                d['senderID'] = ObjectId(d['senderID'])
                                d['time'] = d['time']
                        db[coll].insert_many(data)
