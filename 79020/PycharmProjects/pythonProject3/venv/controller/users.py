from flask import Blueprint,request
from database import *

users_bp=Blueprint('users',__name__,url_prefix='/users')


@users_bp.route('',methods=['POST'])
def register():
    data=request.get_json(force=True)
    account_number=data.get('account_number')
    password=data.get('password')
    return check_and_save(account_number,password)

@users_bp.route('/per_page',methods=['POST'])
def post_infor():
    if session.get('account_number') is not None:
        data = request.get_json(force=True)
        name = data.get('name')
        sex = data.get('sex')
        age = data.get('age')
        conn, cursor = get_connection()
        cursor.execute('update `users` set `name`=%s where account_num=%s', (name, session.get('account_number')))
        cursor.execute('update `users` set `sex`=%s where account_num=%s', (sex, session.get('account_number')))
        cursor.execute('update `users` set `age`=%s where account_num=%s', (age, session.get('account_number')))
        conn.commit()
        cursor.close()
        conn.close()
        return "发布成功！"
    else:
        return "请先登录或注册"


@users_bp.route('/username',methods=['PUT'])
def change_username():
    data=request.get_json(force=True)
    username=data.get('username')
    change_name(username)
    return '修改用户名成功'

@users_bp.route('/password',methods=['PUT'])
def change_password():
    data=request.get_json(force=True)
    password=data.get('password')
    return change_word(password)
@users_bp.route('/check_users',methods=['GET'])
def check_users_infor():
    if session.get('user_id') is None:
        raise HttpError(401,'请先登录')
    return {
            'user_id':session.get('user_id'),
            'username':session.get('username')
        }

@users_bp.route('/admin',methods=['POST'])
def change_message():
    if not str(session.get('account_number')) == '123456':
        raise HttpError(401,'没有管理员权限')
    else:
        data = request.get_json(force=True)
        account_number = data.get('account_number')
        new_message = data.get('new_message')
        ch_message(account_number, new_message)
        return '修改留言成功!'


