from flask import Flask, jsonify, request, session
from mysql.connector import connect
from werkzeug.security import generate_password_hash, check_password_hash
from util import *
import numpy as np
import json


def get_connection():
    conn = connect(user='root', password='', database='bbt3')
    cursor = conn.cursor()
    return conn, cursor


def get_connection2(base):
    conn = connect(user='root', password='', database='bbt3')
    cursor = conn.cursor(buffered=True)
    cursor.execute('select * from `%s`' % (base,))
    result = cursor.fetchall()
    fields = cursor.description
    cursor.close()
    conn.close()
    column_list = []
    for i in fields:
        column_list.append(i[0])
    data = []
    for row in result:
        dict = {}
        for i in range(len(column_list)):
            dict[column_list[i]] = row[i]
        data.append(dict)
    return json.dumps(data, default=str, ensure_ascii=False)


def c_message(content):
    conn, cursor = get_connection()
    cursor.execute('update `users` set `message`=%s where id=%s', (content, session.get('user_id')))
    conn.commit()
    cursor.close()
    conn.close()


def p_message(content):
    conn, cursor = get_connection()
    cursor.execute('update `users` set `message`=%s where account_num=%s', (content, session.get('account_number')))
    conn.commit()
    cursor.close()
    conn.close()


def check_number(account_number):
    conn, cursor = get_connection()
    cursor.execute('select count(*) from `users` where `account_num`=%s', (account_number,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count


def check_info_complete():
    data = request.get_json(force=True)
    if data.get('account_number') is None and data.get('password') is not None:
        raise HttpError(409, '缺少参数account_number')
    elif data.get('password') is None and data.get('account_number') is not None:
        raise HttpError(409, '缺少参数password')
    elif data.get('account_number') is None and data.get('password') is None:
        raise HttpError(409, '缺少参数account_number,password')
    else:
        return True


def check_inf(account_number, password):
    if check_info_complete():
        conn, cursor = get_connection()
        cursor.execute('select `account_num`,`password` from `users` where `account_num`=%s', (account_number,))
        values = cursor.fetchone()
        if values is None:
            raise HttpError(400, '用户名或密码错误')
        account_num = values[0]
        pwd = values[1]
        if not check_password_hash(pwd, password):
            raise HttpError(400, '用户名或密码错误')
        session['account_number'] = account_number
        session['password'] = password
        return "登录成功!"


def check_and_save(account_number, password):
    count = check_number(account_number)

    if count >= 1:
        raise HttpError(409, '已经有该用户！')
    elif count < 1:
        conn, cursor = get_connection()
        cursor.execute('insert into `users`(`account_num`,`password`) values (%s,%s)',
                       (account_number, generate_password_hash(password)))
        conn.commit()
        conn.close()
        cursor.close()
        session['account_number'] = account_number
        return "创建成功!"


def p_comment(comment, account_num):
    conn, cursor = get_connection()
    cursor.execute('insert into `comment`(`account_num`,`comment`,`publisher_num`) values (%s,%s,%s)',
                   (account_num, comment, session.get('account_number')))
    conn.commit()
    cursor.close()
    conn.close()


def like(account_num):
    conn, cursor = get_connection()
    cursor.execute('insert into `likes`(`account_num`,`liker_num`) values (%s,%s)',
                   (account_num, session.get('account_number')))
    conn.commit()
    cursor.close()
    conn.close()


def dislike(account_num):
    conn, cursor = get_connection()
    cursor.execute('delete from `likes` where `account_num`=%s and `liker_num`=%s)',
                   (account_num, session.get('account_number')))
    conn.commit()
    cursor.close()
    conn.close()


def ch_message(account_number, new_message):
    conn, cursor = get_connection()
    cursor.execute('update `users` set `message`=%s where account_num=%s', (new_message, account_number))
    conn.commit()
    cursor.close()
    conn.close()
