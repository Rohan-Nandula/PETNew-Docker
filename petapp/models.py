# models.py

from flask_login import UserMixin
from . import db
from passlib.hash import pbkdf2_sha256 as sha256
import uuid # for public id

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    public_id = db.Column(db.String(50), unique = True)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(10))
    city = db.Column(db.String(100))
    occupation = db.Column(db.String(100))
    password = db.Column(db.String(100))

    """
    Save user details in Database
    """
    def save_record(self):

        db.session.add(self)

        db.session.commit()	

    """
    Find user by name
    """
    @classmethod
    def find_by_name(cls, name):

        return cls.query.filter_by(name=name).first()

    """
    return all the user data in json form available in DB
    """
    @classmethod
    def return_all(cls):

        def to_json(x):

            return {

                'name': x.username,

                'public_id': x.public_id,

                'email': x.email,

                'password': x.password,

                'phone': x.phone,

                'city': x.city,

                'occupation': x.occupation

            }

        return {'users': [to_json(user) for user in UserModel.query.all()]}

    """
    Delete user data
    """
    @classmethod
    def delete_all(cls):

        try:

            num_rows_deleted = db.session.query(cls).delete()

            db.session.commit()

            return {'message': f'{num_rows_deleted} row(s) deleted'}

        except:

            return {'message': 'Something went wrong'}

    """
    generate hash from password by encryption using sha256
    """
    @staticmethod
    def generate_hash(password):

        return sha256.hash(password)

    """
    Verify hash and password
    """
    @staticmethod
    def verify_hash(password, hash_):

        return sha256.verify(password, hash_)
