# !/usr/bin/env python
# -*- coding: utf-8 -*-
# by dsc 2021/04/12
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask_httpauth import HTTPTokenAuth
from config import SECRET_KEY


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:mysql@127.0.0.1:3306/flask"
auth = HTTPTokenAuth()
db = SQLAlchemy(app)


# 建表
class User(db.Model):
    __tablename__ = 'users'  # 表名
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    mobile = db.Column(db.String(128), unique=True)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/token/', methods=['POST'])
def get_token():
    """
    通过手机号验证用户(不需要实现发短信功能)
    :return:{“access_token”: “xxx”, “refresh_token”: “xxx”, “expiry”: 12345}
    """
    # 获取前端请求参数mobile
    mobile = request.form.get('mobile')
    try:
        user = User.query.filter_by(mobile=mobile).first()
        if user:
            serializer = Serializer(SECRET_KEY, expires_in=12345)
            return jsonify(data={'code': 200, 'message': 'Authenticate successfully',
                                 'access_token': serializer.dumps(
                                     {'mobile': '+86-12388888888', 'otp': '123456'}).decode('utf-8'),
                                 'refresh_token': '',
                                 'expiry': 12345})
        else:
            return jsonify(data={'code': 500, 'message': 'Wrong mobile, Authenticate failed'})
    except Exception as e:
        print(e)
        return jsonify(data={'code': 500, 'message': 'Authenticate failed'})


@auth.error_handler
def error_handler():
    return jsonify(data={'code': 401, 'message': '401 Unauthorized Access'})


@auth.verify_token
def verify_token(token):
    """
    解析token
    :param token:
    :return:
    """
    s = Serializer(SECRET_KEY)
    # token正确
    try:
        data = s.loads(token)
        return data
    # token过期
    except SignatureExpired:
        return None
    # token错误
    except BadSignature:
        return None


@auth.login_required
@app.route('/profile/', methods=['GET'])
def get_info():
    """
    获取用户本人基本信息
    :return:
    """
    mobile = request.args.get('mobile')
    try:
        user = User.query.filter_by(mobile=mobile).first()
        if user:
            return jsonify(
                {'code': 200, 'data': {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name}})
        else:
            return jsonify(data={'code': 500, 'message': 'The user does not exist'})
    except Exception as e:
        print(e)
        return jsonify(data={'code': 500, 'message': 'Get failed'})


if __name__ == "__main__":
    # 将host设置为0.0.0.0，则外网用户也可以访问到这个服务
    app.run(host="0.0.0.0", port=5000, debug=True)

