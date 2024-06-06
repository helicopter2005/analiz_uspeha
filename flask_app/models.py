from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<users {self.id}>'


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), default=datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
    content = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<posts {self.id}>"
