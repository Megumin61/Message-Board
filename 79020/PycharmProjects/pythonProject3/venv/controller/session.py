from flask import Blueprint,request
from database import *
session_bp=Blueprint('session',__name__,url_prefix='/session')

@session_bp.route('',methods=['POST'])
def login():
    data=request.get_json(force=True)
    account_number=data.get('account_number')
    password=data.get('password')
    check_inf(account_number,password)
    return '登录成功'