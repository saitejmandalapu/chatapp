import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from flask_login import UserMixin

Base = declarative_base()
   

class Owner(Base, UserMixin):
    __tablename__ = 'ownerDetails'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)    
    email = Column(String(250), unique=True)
    password = Column(String(250), nullable=False)
    is_admin = Column(Boolean, default=False)
   
class Reset_Token(Base):
    __tablename__ = 'reset_tokens'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('ownerDetails.id'))
    token = Column(String(32),nullable=False)                

engine = create_engine('sqlite:///chatapp.db')

Base.metadata.create_all(engine)
