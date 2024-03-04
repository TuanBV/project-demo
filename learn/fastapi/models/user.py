from db.database import Base
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy import Column
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    items = relationship("Article", back_populates="user")