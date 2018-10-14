from database import Base, db_session
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256 as sha256
from marshmallow import Schema, fields



'''
================OTHER RESOURCES================
'''

class DeadlineSchema(Schema):
    id = fields.Integer()
    name = fields.Str(error_messages = {'required':'This field cannot be left blank'}, required = True)
    type = fields.Str(missing=None)
    date = fields.DateTime(error_messages = {'required':'This field cannot be left blank'}, required = True)
    priority = fields.Integer(missing=1)
    num_of_hours = fields.Float(missing=None)
    user_name = fields.Str()

class Deadline(Base):
    __tablename__ = 'deadline'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key = True)
    name = Column(String(120), nullable = False)
    type = Column(String(120))
    date = Column(DateTime)
    priority = Column(Integer)
    num_of_hours = Column(Float)
    user_name = Column(String(120), ForeignKey('user.username'))


    def save_to_db(self):
        db_session.add(self)
        db_session.commit()

    @classmethod
    def find_by_name(cls, name):
       return cls.query.filter_by(name = name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

    @classmethod
    def find_all_ids_of_user(cls, username):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password
            }
        return cls.query.filter_by(user_name = username).with_entities(Deadline.id).all()

    @classmethod
    def delete_all(cls):
      try:
          num_rows_deleted = db_session.query(cls).delete()
          db_session.commit()
          return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
      except:
          return {'message': 'Something went wrong'}

'''
================AUTH RESOURCES================
'''
#declare schemas
class UserSchema(Schema):
    username = fields.Str(error_messages = {'required':'This field cannot be left blank'}, required = True)
    password = fields.Str(error_messages = {'required':'This field cannot be left blank'}, required = True)
    email = fields.Str(missing=None)
    deadlines = fields.Nested(DeadlineSchema, only=['id'], many=True)

#represents users
class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key = True)
    username = Column(String(120), unique = True, nullable = False)
    password = Column(String(120), nullable = False)
    email = Column(String(120))
    deadlines = relationship("Deadline", order_by=Deadline.id, backref="user")

    def save_to_db(self):
        db_session.add(self)
        db_session.commit()

    @classmethod
    def find_by_username(cls, username):
       return cls.query.filter_by(username = username).first()

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db_session.query(cls).delete()
            db_session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
