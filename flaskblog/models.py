from flask import current_app as app
from flaskblog import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg')
    password = db.Column(db.String, nullable=False)
    posts = db.relationship('Post',backref="author",lazy=True)

    def get_reset_token(self,expires_sec=1800):
        s= Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s= Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

# tags = db.Table('tags',
#     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
#     db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
# )


class Post(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text,  nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    tags = db.relationship('Tag', secondary='post_tag')

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted})"

class Tag(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    posts = db.relationship('Post', secondary='post_tag')

class PostTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    posts = db.relationship('Post', backref="posts")
    tags = db.relationship('Tag', backref="tags")