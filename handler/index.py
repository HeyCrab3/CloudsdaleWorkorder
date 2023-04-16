import base64
import json
from flask import Flask, render_template, jsonify, Blueprint, redirect, request, session

from db import db
import time
import requests
import threading
from geetest_config import GEETEST_ID, GEETEST_KEY, REDIS_HOST, REDIS_PORT, CYCLE_TIME, BYPASS_URL, \
    GEETEST_BYPASS_STATUS_KEY
from flask import app
from sdk.geetest_lib import GeetestLib

bp = Blueprint('index', __name__)


@bp.route('/')
def indexPage():
    token = session.get('user_token')
    if token:
        userName = base64.b64decode(token).decode('utf-8')
        isAdmin = db.user.find_one({'userName': userName})
        if isAdmin['perm'] >= 5:
            return render_template("index.html", username=userName, isadmin="L")
        return render_template("index.html", username=userName)
    else:
        return render_template("index.html")


@bp.route('/api/question/hot')
def hotQA():
    result = db.wiki.find_one({'title': '常见的问题'})
    return jsonify({'code': 0, 'msg': '一切正常！', 'result': result['child']})


# New Code Start

@bp.route('/app/config')
def appConfig():
    if app.Debug:
        return jsonify({
            'product': 'HelpDesk',
            'version': 1,
            'isInDevelopmentMode': True,
            'isNextGUI': True
        })
    else:
        return jsonify({
            'product': 'HelpDesk',
            'version': 1,
            'isInDevelopmentMode': False,
            'isNextGUI': True
        })
# New Code End
