from projectapp import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique=True, nullable = False)
	email = db.Column(db.String(120), unique=True, nullable = False)
	password = db.Column(db.String(60), nullable=False)
	image_file = db.Column(db.String(20), unique=False, nullable=False, default='default.jpg')
	records = db.relationship('Audio', backref='user_rec', lazy=True)

	def __repr__(self):
		return f"User('{self.username}','{self.email}','{self.image_file}')"

class Audio(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	record_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	classification = db.Column(db.String(60),unique=False, nullable=False)
	audio = db.Column(db.String(20),unique=False, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	def __repr__(self):
		return f"Audio('{self.audio}','{self.record_date}')"	
