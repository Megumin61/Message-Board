from flask import Flask, jsonify, request, session
from mysql.connector import connect
from werkzeug.security import generate_password_hash, check_password_hash
import json
import numpy as np
from flask_cors import CORS

from database import *
from controller.users import users_bp
from controller.session import session_bp
from util import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
CORS(app, supports_credentials=True)
app.config["SESSION_COOKIE_SAMESITE"] = "None"


@app.route('/')
def get_message():
    data1 = get_connection2('users')
    data2 = get_connection2("comment")
    data3 = get_connection2("likes")
    return 'users:' + data1 + 'comment:' + data2 + 'likes:' + data3 + "现在登陆的是: {}".format(session.get('account_number'))


# ensure_ascii=False
@app.route('/comment', methods=['PUT', 'POST'])
def post_comment():
    if session.get('account_number') is None:
        raise HttpError(401, '请先登录或注册')
    else:
        data = request.get_json(force=True)
        comment = data.get('comment')
        account_num = data.get('account_number')
        p_comment(comment, account_num)
        return '发布成功!'


@app.route('/message', methods=['PUT', 'POST'])
def post_message():
    if session.get('account_number') is None:
        raise HttpError(401, '请先登录或注册')
    else:
        data = request.get_json(force=True)
        content = data.get('content')
        p_message(content)
        return '发布成功!'


@app.route('/message/like', methods=['PUT', 'POST'])
def thumbs():
    if session.get('account_number') is None:
        raise HttpError(401, '请先登录或注册')
    else:
        data = request.get_json(force=True)
        account_num = data.get('account_number')
        like(account_num)
        return '点赞成功!'


@app.route('/message/dislike', methods=['PUT', 'POST'])
def d_thumbs():
    if session.get('account_number') is None:
        raise HttpError(401, '请先登录或注册')
    else:
        data = request.get_json(force=True)
        account_num = data.get('account_number')
        dislike(account_num)
        return '取消点赞成功!'


@app.errorhandler(HttpError)
def handle_http_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


# 注册,改名字,改密码
app.register_blueprint(users_bp)
# 登录
app.register_blueprint(session_bp)
if __name__ == '__main__':
    app.run()
