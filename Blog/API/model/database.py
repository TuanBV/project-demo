from db.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from common.kbn import IntEnum, FlgDelete

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    title = Column(String)
    content = Column(String)
    regist_user = Column(String)
    regist_date = Column(DateTime)
    update_user = Column(String)
    update_date = Column(DateTime)
    flg_del = Column(IntEnum(FlgDelete))