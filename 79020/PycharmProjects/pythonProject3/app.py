from flask import Flask,jsonify,request,session
from mysql.connector import connect
from werkzeug.security import generate_password_hash,check_password_hash
import json
import numpy as np
from database import *
from controller.users import users_bp
from controller.session import session_bp
from util import *
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

@app.route('/')
def get_message():
    conn = connect(user='root', password='', database='bbt3')
    cursor = conn.cursor(buffered=True)
    cursor.execute('select * from `users`')
    result = cursor.fetchall()
    fields = cursor.description
    cursor.close()
    conn.close()
    column_list = []
    for i in fields:
        column_list.append(i[0])
    data=[]
    for row in result:
        dict = {}
        for i in range(len(column_list)):
            dict[column_list[i]] = row[i]
        data.append(dict)
    return json.dumps(data, default=str, ensure_ascii=False)
#ensure_ascii=False

@app.route('/change_message',methods=['PUT'])
def change_message():
    if session.get('account_number') is None:
        raise HttpError(401,'请先登录或注册')
    data = request.get_json(force=True)
    content = data.get('content')
    c_message(content)
    return '修改成功!'

@app.route('/post_message',methods=['POST'])
def post_message():
    if session.get('account_number') is None:
        raise HttpError(401,'请先登录或注册')
    else:
        data = request.get_json(force=True)
        content = data.get('content')
        p_message(content)
        return '发布成功!'

@app.errorhandler(HttpError)
def handle_http_error(error):
    response=jsonify(error.to_dict())
    response.status_code=error.status_code
    return response
#注册,改名字,改密码
app.register_blueprint(users_bp)
#登录
app.register_blueprint(session_bp)
if __name__ =='__main__':
    app.run()
