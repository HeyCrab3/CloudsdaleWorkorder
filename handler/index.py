import base64
from flask import Flask, render_template, jsonify, Bluepoint, Blueprint, redirect, request, session
from db import db
import uuid

bp = Blueprint('index', __name__)


@bp.route('/')
def indexPage():
    token = session.get('user_token')
    if token:
        userName = base64.b64decode(token).decode('utf-8')
        isAdmin = db.user.find_one({'userName': userName})
        if isAdmin['perm'] >= 5:
            return render_template("index.html", username=userName, admin="L")
        return render_template("index.html", username=userName)
    else:
        return render_template("index.html")


@bp.route('/api/question/hot')
def hotQA():
    result = db.wiki.find_one({'title': '常见的问题'})
    return jsonify({'code': 0, 'msg': '一切正常！', 'result': result['child']})
