import base64
import datetime
import json

from flask import Flask, render_template, jsonify, Blueprint, redirect, request, session
from db import db
from bson import json_util, ObjectId
import uuid

bp = Blueprint('ticket', __name__)


def find(username):
    users = list(db.user.find({'userName': username}))
    for user in users:
        if user['userName'] == username:
            return user
    return None


def parse_json(data):
    return json.loads(json_util.dumps(data))


# 这个逻辑是用来看用户是不是登录的
@bp.route('/ticket')
def TicketHome():
    token = session.get('user_token')
    if token is None:
        session.clear()
        return render_template('error.html', msg='你没有登录'),401
    else:
        isExist = find(base64.b64decode(token).decode('utf-8'))
        if isExist is None:
            return render_template('error.html', msg='会话无效'),401
        else:
            return redirect('/ticket/overview')


# 工单主页逻辑
@bp.route('/ticket/overview')
def TicketOverview():
    user_token = session['user_token']
    if user_token is None:
        session.clear()
        return render_template('error.html', msg='你没有登录'),401
    else:
        isExist = find(base64.b64decode(user_token).decode('utf-8'))
        if isExist is None:
            return render_template('error.html', msg='会话无效'),401
        else:
            return render_template('overview.html', username=base64.b64decode(user_token).decode('utf-8'))

# New Code STart

@bp.route('/api/ticket/metadata')
def TicketMetadata():
    # 鉴权
    user_token = session['user_token']
    if user_token is None:
        session.clear()
        return jsonify({'code': 403, 'msg': '无效会话'})
    else:
        isExist = find(base64.b64decode(user_token).decode('utf-8'))
        if isExist is None:
            return jsonify({'code': 403, 'msg': '无效会话'})
        else:
            # 检查用户权限
            if isExist['perm'] <= 5:
                return jsonify({'code': 403, 'msg': '权限不够'})
            else:
                ticket_id = request.args.get('ticket_id')
                result = parse_json(db.workorder.find_one({'_id': ObjectId(ticket_id)}))
                return jsonify({'code': 0, 'msg': '操作成功', 'data': result})

@bp.route('/api/ticket/delete', methods=['POST'])
def DeleteTicket():
    user_token = session['user_token']
    if user_token is None:
        session.clear()
        return jsonify({'code': 403, 'msg': '无效会话'})
    else:
        isExist = find(base64.b64decode(user_token).decode('utf-8'))
        if isExist is None:
            return jsonify({'code': 403, 'msg': '无效会话'})
        else:
            a = request.get_json()
            ticketid = a.get('ticket_id')
            if isExist['perm'] < 5:
                isThisGuy = db.workorder.find_one({'_id': ObjectId(ticketid)})
                isThisGuy = parse_json(isThisGuy)
                if isThisGuy['sender'] != base64.b64decode(user_token).decode('utf-8'):
                    return jsonify({'code': 403, 'msg': '不能删除不属于你的工单'})
                else:
                    try:
                        db.workorder.delete_one({'_id': ObjectId(ticketid)})
                        return jsonify({'code': 0, 'msg': '删除成功。'})
                    except:
                        return jsonify({'code': 500, 'msg': '发生错误！'})
            else:
                db.workorder.delete_one({'_id': ObjectId(ticketid)})
                return jsonify({'code': 0, 'msg': '删除成功。'})

# New Code End

@bp.route('/api/ticket/overall')
def TicketAPIStatus():
    user_token = session['user_token']
    if user_token is None:
        session.clear()
        return jsonify({'code': 403, 'msg': '无效会话'})
    else:
        isExist = find(base64.b64decode(user_token).decode('utf-8'))
        if isExist is None:
            return jsonify({'code': 403, 'msg': '无效会话'})
        else:
            platformTicketNum = db.workorder.count_documents({})
            userTicketNum = db.workorder.count_documents({'sender': base64.b64decode(user_token).decode('utf-8')})
            processingNum = db.workorder.count_documents(
                {'sender': base64.b64decode(user_token).decode('utf-8'), 'status': 1})
            closeNum = db.workorder.count_documents(
                {'sender': base64.b64decode(user_token).decode('utf-8'), 'status': -1})
            userPerm = find(base64.b64decode(user_token).decode('utf-8'))
            if userPerm['perm'] == 1:
                userPerm = "普通用户"
            elif userPerm['perm'] == 5:
                userPerm = "客服"
            elif userPerm['perm'] == 6:
                userPerm = "志愿"
            elif userPerm['perm'] == 10:
                userPerm = "运维/管理/服主"
            return jsonify(
                {'code': 0, 'msg': '一切正常！', 'platformTicketNum': platformTicketNum, 'userTicketNum': userTicketNum,
                 'processingNum': processingNum, 'closeNum': closeNum, 'userPerm': userPerm})


@bp.route('/api/ticket/myticket')
def MyTicket():
    user_token = session['user_token']
    if user_token is None:
        session.clear()
        return jsonify({'code': 403, 'msg': '无效会话'})
    else:
        isExist = find(base64.b64decode(user_token).decode('utf-8'))
        if isExist is None:
            return jsonify({'code': 403, 'msg': '无效会话'})
        else:
            userPerm = find(base64.b64decode(user_token).decode('utf-8'))
            if userPerm['perm'] == 1:
                result = parse_json(db.workorder.find({'sender': userPerm['userName']}))
            else:
                result = parse_json(db.workorder.find())
            return jsonify(
                {'code': 0, 'msg': '一切正常！', 'ticketList': result})


@bp.route('/ticket/new')
def NewTicket():
    user_token = session['user_token']
    if user_token is None:
        session.clear()
        return render_template('error.html', msg='你没有登录'),401
    else:
        isExist = find(base64.b64decode(user_token).decode('utf-8'))
        if isExist is None:
            return render_template('error.html', msg='会话无效'),401
        else:
            return render_template('newticket.html', username=base64.b64decode(user_token).decode('utf-8'))


@bp.route('/api/ticket/new', methods=['POST'])
def NewTicketAPI():
    user_token = session['user_token']
    if user_token is None:
        session.clear()
        return jsonify({'code': 403, 'msg': '无效会话'})
    else:
        isExist = find(base64.b64decode(user_token).decode('utf-8'))
        if isExist is None:
            return jsonify({'code': 403, 'msg': '无效会话'})
        else:
            a = request.get_json()
            title = a.get('title')
            content = a.get('content')
            images = a.get('images[]')
            print(images)
            data = {'title': title, 'content': content, 'sender': base64.b64decode(user_token).decode('utf-8'),
                    'senderID': isExist['_id'], 'status': 0,
                    'time': datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                    'images': images}
            db.workorder.insert_one(data)
            return jsonify({'code': 0, 'msg': '工单添加成功！正在重定向到首页..'})


@bp.route('/ticket/view')
def ViewTicket():
    user_token = session['user_token']
    if user_token is None:
        session.clear()
        return render_template('error.html', msg='你没有登录'),401
    else:
        isExist = find(base64.b64decode(user_token).decode('utf-8'))
        if isExist is None:
            return render_template('error.html', msg='会话无效'),401
        else:
            ticketID = request.args.get('id')
            return render_template('view.html', username=base64.b64decode(user_token).decode('utf-8'), ticketID=ticketID)

@bp.route('/api/ticket/reply')
def TicketReply():
    user_token = session['user_token']
    if user_token is None:
        session.clear()
        return jsonify({'code': 403, 'msg': '无效会话'}),401
    else:
        isExist = find(base64.b64decode(user_token).decode('utf-8'))
        if isExist is None:
            return jsonify({'code': 403, 'msg': '无效会话'})
        else:
            ticketid = request.args.get('id')
            result = db.reply.find({'replyTo': ticketid})
            result = parse_json(result)
            if isExist['perm'] < 5:
                isThisGuy = db.workorder.find_one({'_id': ObjectId(ticketid)})
                isThisGuy = parse_json(isThisGuy)
                if isThisGuy['sender'] != base64.b64decode(user_token).decode('utf-8'):
                    return jsonify({'code': 403, 'msg': '这不是你的工单，无法查看。', 'reply': None})
                else:
                    return jsonify({'code': 0, 'msg': '一切正常！', 'reply': result})
            else:
                return jsonify({'code': 0, 'msg': '一切正常！', 'reply': result})

@bp.route('/api/ticket/ticketdata')
def TicketData():
    user_token = session['user_token']
    if user_token is None:
        session.clear()
        return jsonify({'code': 403, 'msg': '无效会话'})
    else:
        isExist = find(base64.b64decode(user_token).decode('utf-8'))
        if isExist is None:
            return jsonify({'code': 403, 'msg': '无效会话'})
        else:
            ticketid = request.args.get('id')
            result = db.workorder.find_one({'_id': ObjectId(ticketid)})
            result = parse_json(result)
            if isExist['perm'] < 5:
                if result['sender'] != base64.b64decode(user_token).decode('utf-8'):
                    x = jsonify({'code': 403, 'msg': '这不是你的工单，无法查看。', 'data': None})
                    return x,403
                else:
                    return jsonify({'code': 0, 'msg': '一切正常！', 'data': result})
            else:
                return jsonify({'code': 0, 'msg': '一切正常！', 'data': result})

@bp.route('/api/ticket/sendreply', methods=['POST'])
def NewTicketReply():
    user_token = session['user_token']
    if user_token is None:
        session.clear()
        return jsonify({'code': 403, 'msg': '无效会话'})
    else:
        isExist = find(base64.b64decode(user_token).decode('utf-8'))
        if isExist is None:
            return jsonify({'code': 403, 'msg': '无效会话'})
        else:
            a = request.get_json()
            ticketid = request.args.get('id')
            content = a.get('content')
            isThisGuy = db.workorder.find_one({'_id': ObjectId(ticketid)})
            isThisGuy = parse_json(isThisGuy)
            if isThisGuy['sender'] != base64.b64decode(user_token).decode('utf-8'):
                isAdmin = db.user.find_one({'userName':base64.b64decode(user_token).decode('utf-8')})
                if isAdmin['perm'] >= 5:
                    if isThisGuy['status'] == -1:
                        return jsonify({'code': 400, 'msg': '工单已关闭，禁止操作'})
                    else:
                        data = {'replyTo': ticketid, 'content': content,
                                'sender': base64.b64decode(user_token).decode('utf-8'), 'senderID': user['_id'],
                                'time': datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), 'isAdmin': True}
                        db.reply.insert_one(data)
                        return jsonify({'code': 0, 'msg': '回复发送成功'})
                else:
                    return jsonify({'code': 403, 'msg': '这不是你的工单，无法回复。'})
            else:
                user = find(base64.b64decode(user_token).decode('utf-8'))
                if isThisGuy['status'] == -1:
                    return jsonify({'code': 400, 'msg': '工单已关闭，禁止操作'})
                else:
                    data = {'replyTo': ticketid, 'content': content,
                            'sender': base64.b64decode(user_token).decode('utf-8'), 'senderID': user['_id'],
                            'time': datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), 'isAdmin': False}
                    db.reply.insert_one(data)
                    return jsonify({'code': 0, 'msg': '回复发送成功'})
