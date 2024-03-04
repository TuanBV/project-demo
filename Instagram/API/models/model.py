from db.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from utils.kbn import IntEnum, FlgDelete


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    full_name = Column(String)
    flg_del = Column(IntEnum(FlgDelete), default=FlgDelete.OFF.value)
    items = relationship('Post', back_populates='user')


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    image_url_type = Column(String)
    caption = Column(String)
    timestamp = Column(DateTime)
    flg_del = Column(IntEnum(FlgDelete), default=FlgDelete.OFF.value)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='items')
    comment = relationship('Comment', back_populates='post')

class Comment(Base):
    __tablename__='comment'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    username = Column(String)
    timestamp = Column(DateTime)
    flg_del = Column(IntEnum(FlgDelete), default=FlgDelete.OFF.value)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship('Post', back_populates='comment')