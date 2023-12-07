from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime
from movielist import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Movie(db.Model): # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True, unique=True) # 主键
    Title = db.Column(db.String(255), nullable = False) # 电影标题
    Date = db.Column(db.DateTime) # 上映日期
    Country = db.Column(db.String(10)) # 电影国家
    Genre = db.Column(db.String(10)) # 电影类型
    Year = db.Column(db.String(4)) # 电影年份

