import base64
import json

from bson import json_util
from flask import Flask, render_template, jsonify, Bluepoint, Blueprint, redirect, request, session
from db import db
import uuid
import hashlib

bp = Blueprint('user', __name__)
def find(username):
    '''
        根据用户名查找是否已经注册，如果是，返回用户的全部信息，如果不是，返回None
    '''
    users = list(db.user.find({'userName': username}))
    for user in users:
        if user['userName'] == username:
            return user
    return None


def findbyplayerID(username):
    '''
        根据玩家ID查找是否已经注册，如果是，返回用户的全部信息，如果不是，返回None
    '''
    users = list(db.user.find({'gameID': username}))
    for user in users:
        if user['gameID'] == username:
            return user
    return None


def parse_json(data):
    return json.loads(json_util.dumps(data))


@bp.route('/user/login')
def login():
    return render_template('login.html')
@bp.route('/api/user/login',methods=['POST'])
def sessionL():
    userName = request.form.get('userName')
    passWord = request.form.get('passWord')
    captchaCode = request.form.get('captcha')
    verify = session['imageCode']
    result = db.user.find_one({'userName':userName})
    if result:
        if hashlib.sha256(passWord.encode('utf-8')).hexdigest() == result['passWord']:
            if captchaCode == verify:
                session['user_token'] = base64.b64encode(userName.encode('utf-8'))
                session['device_code'] = base64.b64encode(str(uuid.uuid4()).encode('utf-8'))
                return jsonify({'code':0,'msg':'欢迎回来，' + result['userName']})
            else:
                return jsonify({'code': 20001, 'msg': '验证码错误'})
        else:
            return jsonify({'code': 20000, 'msg': '密码错误'})
    else:
        return jsonify({'code': 10010, 'msg': '账户不存在！请先注册一个'})
@bp.route('/user/reg')
def regInterface():
    return render_template('reg.html')
@bp.route('/api/user/reg',methods=['POST'])
def regApi():
    userName = request.form.get('userName')
    passWord = request.form.get('passWord')
    gameID = request.form.get('gameID')
    nickName = request.form.get('nickName')
    captchaCode = request.form.get('captcha')
    verify = session['imageCode']
    isRegistered = find(userName)
    if isRegistered != None:
        return jsonify({'code': 1002, 'msg': '用户名已存在'})
    else:
        isGameIDBind = findbyplayerID(gameID)
        if isGameIDBind:
            return jsonify({'code': 1003, 'msg': '游戏ID已被用户 ' + isGameIDBind['userName'] + " 绑定，如果这不是你的账号，请联系管理员！"})
    if captchaCode == verify:
        data = {'userName': userName, 'passWord': hashlib.sha256(passWord.encode('utf-8')).hexdigest(), 'gameID': gameID,'perm': 1,'nickName': nickName}
        db.user.insert_one(data)
        return jsonify({'code': 0, 'msg': '注册成功，正在跳转登录页...'})
    else:
        return jsonify({'code': 20001, 'msg': '验证码错误'})


@bp.route('/api/logout')
def logOUT():
    session.clear()
    return "您已成功退出 <a href='/'>回到主页</a>"


@bp.route('/user')
def user():
    user_token = session['user_token']
    if user_token is None:
        session.clear()
        return render_template('error.html', msg='你没有登录'), 401
    else:
        isExist = find(base64.b64decode(user_token).decode('utf-8'))
        if isExist is None:
            return render_template('error.html', msg='会话无效'), 401
        else:
            return render_template('user.html', username=base64.b64decode(user_token).decode('utf-8'))


@bp.route('/api/user/me')
def me():
    user_token = session['user_token']
    if user_token is None:
        session.clear()
        return jsonify({'code': 403, 'msg': '无效会话'}), 401
    else:
        isExist = find(base64.b64decode(user_token).decode('utf-8'))
        if isExist is None:
            return jsonify({'code': 403, 'msg': '无效会话'}), 401
        else:
            userData = find(base64.b64decode(user_token).decode('utf-8'))
            userData = parse_json(userData)
            return jsonify({'code': 0, 'msg': '操作成功', 'userdata': userData})

@bp.route('/api/user/changepwd',methods=['POST'])
def UserChangePwd():
    user_token = session['user_token']
    if user_token is None:
        session.clear()
        return jsonify({'code': 403, 'msg': '无效会话'}), 401
    else:
        isExist = find(base64.b64decode(user_token).decode('utf-8'))
        if isExist is None:
            return jsonify({'code': 403, 'msg': '无效会话'}), 401
        else:
            newPwd = request.form.get('newPwd')
            db.user.update_one({'userName': base64.b64decode(user_token).decode('utf-8')}, {'$set': {'passWord': hashlib.sha256(newPwd.encode('utf-8')).hexdigest()}})
            return jsonify({'code': 0, 'msg': '密码修改成功'})

@bp.route('/api/user/changenick',methods=['POST'])
def UserChangeNick():
    user_token = session['user_token']
    if user_token is None:
        session.clear()
        return jsonify({'code': 403, 'msg': '无效会话'}), 401
    else:
        isExist = find(base64.b64decode(user_token).decode('utf-8'))
        if isExist is None:
            return jsonify({'code': 403, 'msg': '无效会话'}), 401
        else:
            newNick = request.form.get('newNick')
            db.user.update_one({'userName': base64.b64decode(user_token).decode('utf-8')}, {'$set': {'nickName': newNick}})
            return jsonify({'code': 0, 'msg': '昵称修改成功'})
