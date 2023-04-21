from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    camera = db.relationship('Camera', backref='camera', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Client(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    payment_information = db.Column(db.String(255))
    address = db.relationship('MailingAddress', backref='address', lazy='dynamic')
    shoot = db.relationship('Shoot', backref='shoot', lazy='dynamic')

    def __repr__(self):
        return '<Client {}>'.format(self.first_name)

class MailingAddress(db.Model):
    __tablename__ = 'mailing_addresses'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.street)
    
class Shoot(db.Model):
    __tablename__ = 'shoot_information'
    id = db.Column(db.Integer, primary_key=True)
    locations = db.Column(db.String)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    time = db.Column(db.String)
    prompt = db.Column(db.String)
    equipment = db.Column(db.String)
    num_photos_requested = db.Column(db.Integer)
    model_release = db.Column(db.String) # enter yes or no if model release has been submitted
    branding = db.Column(db.String) # link to branding/graphics

# next add photos database w/ smugmug api

class Camera(db.Model):
    __tablename__ = 'camera'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String)
    model = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lens = db.relationship('Lens', backref='lens', lazy='dynamic')

class Lens(db.Model):
    __tablename__ = 'lens'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String)
    model = db.Column(db.String)
    camera_id = db.Column(db.Integer, db.ForeignKey('camera.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))