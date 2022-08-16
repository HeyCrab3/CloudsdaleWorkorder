import base64
from flask import Flask, render_template, jsonify, Bluepoint, Blueprint, redirect, request, session
from db import db
import uuid

bp = Blueprint('wiki', __name__)
@bp.route('/wiki')
def wiki():
    token = session.get('user_token')
    if token:
        userName = base64.b64decode(token).decode('utf-8')
        return render_template("wiki.html", username=userName)
    else:
        return render_template("wiki.html")#