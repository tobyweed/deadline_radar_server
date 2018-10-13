from database import Base, db_session
from sqlalchemy import Column, Integer, String, DateTime, Float

from marshmallow import Schema, fields

class DeadlineSchema(Schema):
    id = fields.Integer()
    name = fields.Str(error_messages = {'required':'This field cannot be left blank'}, required = True)
    type = fields.Str(missing=None)
    date = fields.DateTime(error_messages = {'required':'This field cannot be left blank'}, required = True)
    priority = fields.Integer(missing=1)
    num_of_hours = fields.Float(missing=None)

class Deadline(Base):
    __tablename__ = 'deadline'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key = True)
    name = Column(String(120), nullable = False)
    type = Column(String(120))
    date = Column(DateTime)
    priority = Column(Integer)
    num_of_hours = Column(Float)


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
    def delete_all(cls):
      try:
          num_rows_deleted = db_session.query(cls).delete()
          db_session.commit()
          return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
      except:
          return {'message': 'Something went wrong'}
