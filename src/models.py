import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    usarname = Column(String(250), nullable=False)
    name = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(20), nullable = False)


    post = relationship('Post', back_populates = 'user')
    comments = relationship('Comments', back_populates = 'comments')
    followers = relationship('Follower', foreign_keys='Follower.user_to_id', back_populates = 'user_to')
    following = relationship('Follower', foreign_keys='Follower.user_from_id', back_populates = 'user_from')

class Follower(Base):
    __tablename__ = 'follower'
 
    user_from_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('user.id'), primary_key=True)


    follower = relationship('User', foreign_keys=[user_from_id], back_populates='following')
    followed = relationship('User', foreign_keys=[user_to_id], back_populates='followers')

class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    comment_text = Column(Text, primary_key=True)
    author_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    

    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    body = Column(Text)
    description = Column(Text)


    user = relationship('User', back_populates='posts')
    comment = relationship('Comment', back_populates='posts')

class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    url = Column(String(50), nullable=True)
    type = Column(Enum('image', 'video', name='media_type'), nullable=False)

    post = relationship('Post', back_populates='media')

    
    def to_dict(self):
     return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e

