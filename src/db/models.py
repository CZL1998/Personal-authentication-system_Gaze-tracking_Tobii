# -*- coding:utf-8 -*-

from sqlalchemy import Column, Integer, VARCHAR, Text, Float, DateTime, Double, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(100), nullable=False, comment='账号')
    password = Column(VARCHAR(32), nullable=False, comment='密码')
    gid = Column(Integer, nullable=False)

    # @orm.reconstructor
    def __init__(self, *args, **kwargs):
        if kwargs:
            user = kwargs
        if args:
            user = args
        self.username = user.get('name')
        self.password = user.get('pass')
        self.gid = user.get('gid')

class Gaze(Base):
    __tablename__ = 'gaze'
    gid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(100), nullable=False, unique=True)
    url = Column(Text, nullable=False, unique=True)