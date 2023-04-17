from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
class Client(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    address = db.relationship('MailingAddress', backref='address', lazy='dynamic')

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
    client_id = db.Column(db.Integer, db.ForeignKey(Client.id))

    def __repr__(self):
        return '<Post {}>'.format(self.street)
