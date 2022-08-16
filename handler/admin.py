import base64
import datetime
import json

from flask import Flask, render_template, jsonify, Bluepoint, Blueprint, redirect, request, session
from db import db
from bson import json_util, ObjectId
import uuid

bp = Blueprint('admin', __name__)


def find(username):
    users = list(db.user.find({'userName': username}))
    for user in users:
        if user['userName'] == username:
            return user
    return None


def parse_json(data):
    return json.loads(json_util.dumps(data))

@bp.route('/admin')
def AdminPage():
    user_token = session['user_token']
    if user_token is None:
        return redirect('/')
    else:
        result = find(base64.b64decode(user_token).decode('utf-8'))
        if result['perm'] < 10:
            return redirect('/')
        else:
            return render_template('admin.html', username=base64.b64decode(user_token).decode('utf-8'))

@bp.route('/api/admin/userData')
def AdminUserData():
    user_token = session['user_token']
    if user_token is None:
        return jsonify({'code': 401, 'msg': '无效会话'}), 401
    else:
        result = find(base64.b64decode(user_token).decode('utf-8'))
        if result['perm'] < 10:
            return jsonify({'code': 403, 'msg': '无权访问'}),403
        else:
            result = db.user.find()
            result = parse_json(result)
            return jsonify({'code': 0, 'msg': '很好的工作', 'userdata': result})


@bp.route('/api/admin/ticket/ticketlist')
def MyTicket():
    user_token = session['user_token']
    if user_token is None:
        return jsonify({'code': 401, 'msg': '无效会话'}), 401
    else:
        result = find(base64.b64decode(user_token).decode('utf-8'))
        if result['perm'] < 10:
            return jsonify({'code': 403, 'msg': '无权访问'}), 403
        else:
            userPerm = find(base64.b64decode(user_token).decode('utf-8'))
            if userPerm['perm'] == 1:
                result = parse_json(db.workorder.find({'sender': userPerm['userName']}))
            else:
                result = parse_json(db.workorder.find())
            return jsonify(
                {'code': 0, 'msg': '一切正常！', 'ticketList': result})


@bp.route('/api/admin/readdb')
def AdminDBReader():
    user_token = session['user_token']
    if user_token is None:
        return jsonify({'code': 401, 'msg': '无效会话'}), 401
    else:
        result = find(base64.b64decode(user_token).decode('utf-8'))
        if result['perm'] < 10:
            return jsonify({'code': 403, 'msg': '无权访问'}),403
        else:
            db1 = request.args.get('db')
            if db1 == "workorder":
                result = db.workorder.find()
                result = parse_json(result)
                return jsonify({'code': 0, 'msg': '数据库读取成功', 'result': result})
            elif db1 == "user":
                result = db.user.find()
                result = parse_json(result)
                return jsonify({'code': 0, 'msg': '数据库读取成功', 'result': result})
            elif db1 == "reply":
                result = db.reply.find()
                result = parse_json(result)
                return jsonify({'code': 0, 'msg': '数据库读取成功', 'result': result})
            elif db1 == "wiki":
                result = db.wiki.find()
                result = parse_json(result)
                return jsonify({'code': 0, 'msg': '数据库读取成功', 'result': result})
            else:
                return jsonify({'code': 404, 'msg': '这个数据库并不存在', 'result': None})

@bp.route('/api/admin/ticket/reply',methods=['POST'])
def AdminTicketReply():
    user_token = session['user_token']
    if user_token is None:
        return jsonify({'code': 401, 'msg': '无效会话'}), 401
    else:
        result = find(base64.b64decode(user_token).decode('utf-8'))
        if result['perm'] < 10:
            return jsonify({'code': 403, 'msg': '无权访问'}), 403
        else:
            ticketid = request.form.get('ticketID')
            content = request.form.get('reply')
            user = find(base64.b64decode(user_token).decode('utf-8'))
            data = {'replyTo': ticketid, 'content': content, 'sender': base64.b64decode(user_token).decode('utf-8'),
                    'senderID': user['_id'], 'time': datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                    'isAdmin': True}
            db.reply.insert_one(data)
            return jsonify({'code':0, 'msg': '回复发送成功'})
