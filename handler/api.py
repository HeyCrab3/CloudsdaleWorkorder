import base64
import datetime
import json

from flask import Flask, render_template, jsonify, Bluepoint, Blueprint, redirect, request, session, Response
from db import db
from bson import json_util, ObjectId
import uuid

from geetest_config import GEETEST_ID, GEETEST_KEY
from sdk.geetest_lib import GeetestLib

bp = Blueprint('api', __name__)

@bp.route('/api/geetest/getChallenge')
def getGeetestChallenge():
    pass
    gt_lib = GeetestLib(GEETEST_ID, GEETEST_KEY)
    digestmod = "md5"
    user_id = "test"
    param_dict = {"digestmod": digestmod, "user_id": user_id, "client_type": "web", "ip_address": "127.0.0.1"}
    result = gt_lib.register(digestmod, param_dict)
    # 注意，不要更改返回的结构和值类型
    return Response(result.data, content_type='application/json;charset=UTF-8')