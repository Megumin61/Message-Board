from flask import Blueprint,request
from database import *

users_bp=Blueprint('users',__name__,url_prefix='/users')


@users_bp.route('',methods=['POST'])
def register():
    data=request.get_json(force=True)
    account_number=data.get('account_number')
    password=data.get('password')
    return check_and_save(account_number,password)

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
def delete_users():
    data=request.get_json(force=True)
    username=data.get('del_username')
    return de_users(username)

