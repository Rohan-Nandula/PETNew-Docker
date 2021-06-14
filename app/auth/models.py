# Merge changes in packages
from flask_login import UserMixin
from . import db
from werkzeug.security import generate_password_hash as shaGen256, check_password_hash as shaChk256
import shortuuid # for public id


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    public_id = db.Column(db.String(50), unique = True)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(10))
    city = db.Column(db.String(100))
    occupation = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self):
        self.id = None        
        self.name = None
        self.public_id = None
        self.email = None
        self.phone = None
        self.city = None
        self.occupation = None
        self.password = None

    def __repr__(self):
        return '<User %r>' % self.email

    """
    generate hash from password by encryption using sha256
    """
    @staticmethod
    def generate_hash(password):

        return shaGen256.hash(password)

    """
    Verify hash and password
    """
    @staticmethod
    def verify_hash(password, hash_):

        return shaChk256.verify(password, hash_)