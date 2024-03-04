from db.database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String, Integer, Boolean
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="items")