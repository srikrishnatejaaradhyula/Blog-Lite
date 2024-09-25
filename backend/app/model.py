from datetime import datetime
from app import db


class Auth(db.Model):
    __tablename__= 'auth'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(80),nullable=False)


class Profile(db.Model):
    __tablename__= 'profile'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(120),unique=True,nullable=False)
    profile_img = db.Column(db.LargeBinary,nullable=False)
    auth_id = db.Column(db.Integer, db.ForeignKey('auth.id'), nullable=False)
    description = db.Column(db.String(500),nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Post(db.Model):
    __tablename__= 'post'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(120),unique=True,nullable=False)
    description = db.Column(db.String(500),nullable=False)
    post_img = db.Column(db.LargeBinary,nullable=False) 
    auth_id = db.Column(db.Integer, db.ForeignKey('auth.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Comment(db.Model):
    __tablename__= 'comment'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    comment = db.Column(db.String(120),nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    auth_id = db.Column(db.Integer, db.ForeignKey('auth.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Like(db.Model):
    __tablename__= 'like'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    auth_id = db.Column(db.Integer, db.ForeignKey('auth.id'), nullable=False)

class Follow(db.Model):
    __tablename__= 'follow'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('auth.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('auth.id'), nullable=False)


