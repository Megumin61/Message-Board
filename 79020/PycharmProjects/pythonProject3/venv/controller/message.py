from flask import Blueprint, request
from database import *

message_bp = Blueprint('message', __name__, url_prefix='/message')



@users_bp.route('/post_passage',methods=['POST'])
def post_passage():
    data=request.get_json(force=True)
    content=data.get('content')
    permission = data.get('permission')
    if permission =="private":
        conn, cursor = get_connection()
        cursor.execute('update `users` set `permission`=%s where id=%s', (int(1), session.get('user_id')))
        conn.commit()
        cursor.close()
        conn.close()
    else:
        conn, cursor = get_connection()
        cursor.execute('update `users` set `permission`=%s where id=%s', (int(0), session.get('user_id')))
        conn.commit()
        cursor.close()
        conn.close()
    p_passage(content,permission)
    return '发布成功！'
@users_bp.route('/change_passage',methods=['PUT'])
def change_passage():
    data = request.get_json(force=True)
    content = data.get('content')
    c_passage(content)
    return '修改成功!'
@users_bp.route('/delete_passage',methods=['PUT'])
def delete_passage():
    data = request.get_json(force=True)
    content = data.get('content')
    d_passage(content)
    return '删除成功!'
@users_bp.route('/get_passage',methods=['GET'])
def get_passage():
    conn, cursor = get_connection()
    cursor.execute('select `passages` from `users` where `id`=%s', (session.get('user_id'),))
    content=cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return content