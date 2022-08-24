import json

from flask import Flask, jsonify
from db import data_import
from handler import user, captcha, index, wiki, workorder, admin, api

import time
import redis
import requests
import threading

from geetest_config import GEETEST_ID, GEETEST_KEY, REDIS_HOST, REDIS_PORT, CYCLE_TIME, BYPASS_URL, \
    GEETEST_BYPASS_STATUS_KEY
from handler.index import redis_connect

from sdk.geetest_lib import GeetestLib

app = Flask(__name__)


# 别动。极验验证码相关模块
# 建立redis连接池
def init_redis_connect():
    try:
        host = REDIS_HOST
        port = REDIS_PORT
        pool = redis.ConnectionPool(host=host, port=port)
        redis_connect = redis.Redis(connection_pool=pool)
        return redis_connect
    except Exception as e:
        return None

redis_connect = init_redis_connect()

# 发送bypass请求，获取bypass状态并进行缓存（如何缓存可根据自身情况合理选择,这里是使用redis进行缓存）
def check_bypass_status():
    while True:
        response = ""
        params = {"gt": GEETEST_ID}
        try:
            response = requests.get(url=BYPASS_URL, params=params)
        except Exception as e:
            print(e)
        if response and response.status_code == 200:
            print(response.content)
            bypass_status_str = response.content.decode("utf-8")
            bypass_status = json.loads(bypass_status_str).get("status")
            redis_connect.set(GEETEST_BYPASS_STATUS_KEY, bypass_status)
        else:
            bypass_status = "fail"
            redis_connect.set(GEETEST_BYPASS_STATUS_KEY, bypass_status)
        print("bypass状态已经获取并存入redis，当前状态为-{}".format(bypass_status))
        time.sleep(CYCLE_TIME)


def get_bypass_cache():
    bypass_status_cache = redis_connect.get(GEETEST_BYPASS_STATUS_KEY)
    bypass_status = bypass_status_cache.decode("utf-8")
    return bypass_status


app.debug = True
app.config['SECRET_KEY'] = b'45r3aug435qy95t3hu9pg4tyui4teabyiuybuegrbergrgiuhpergauh'

# 系统初始化后请禁用该函数，否则程序重启后将会清除数据库
# with app.app_context():
#    data_import()

# 注册蓝图
app.register_blueprint(user.bp)
app.register_blueprint(captcha.bp)
app.register_blueprint(index.bp)
app.register_blueprint(wiki.bp)
app.register_blueprint(workorder.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(api.bp)

# 设置500错误处理器
@app.errorhandler(500)
def server_error(e):
    return jsonify({"code": 500, "msg": "Server Internal Error", "error": e})


# 设置404错误处理器
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"code": 404, "msg": "Not Found", "error": None})


# 启动服务器程序
if __name__ == '__main__':
    app.run(host='192.168.3.15', port=24650)

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
