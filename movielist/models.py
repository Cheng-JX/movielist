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
    Title = db.Column(db.String(255), nullable = False, unique=True) # 电影标题
    Date = db.Column(db.DateTime) # 上映日期
    Country = db.Column(db.String(10)) # 电影国家
    Genre = db.Column(db.String(10)) # 电影类型
    Year = db.Column(db.String(4)) # 电影年份

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    Name = db.Column(db.String(50), nullable=False)
    Gender = db.Column(db.String(2), nullable=False)
    Country = db.Column(db.String(50))

class Relation(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), nullable=False)
    type = db.Column(db.String(20))

    # 定义关系
    movie = db.relationship('Movie', back_populates='relations')
    actor = db.relationship('Actor', back_populates='relations')

# 在 Movie 和 Actor 模型中添加关系
Movie.relations = db.relationship('Relation', back_populates='movie')
Actor.relations = db.relationship('Relation', back_populates='actor')

class MovieBox(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True) # 主键
    Box = db.Column(db.Float)

#class ActorBox(db.Model):
    #id = db.Column(db.Integer, primary_key=True, unique=True) # 主键
    #Box = db.Column(db.Float)