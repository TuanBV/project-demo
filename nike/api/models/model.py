from db.database import Base
from utils.kbn import IntEnum, FlgDelete, ROLE
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    """
        Model user
    """
    __tablename__ = 'user'
    user_id = Column(String(20), primary_key=True)
    username = Column(String(256), nullable=False)
    email = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)
    fullname = Column(String(256), nullable=False)
    area = Column(String(256), nullable=True)
    city = Column(String(256), nullable=True)
    state = Column(String(256), nullable=True)
    postcode = Column(String(10), nullable=True)
    token = Column(String(1000), nullable=True)
    birthday = Column(DateTime, nullable=True)
    role = Column(IntEnum(ROLE), default=ROLE.USER)
    created_user = Column(String(256))
    created_date = Column(DateTime, default=func.now())
    updated_user = Column(String(256))
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    flg_del = Column(IntEnum(FlgDelete), default=FlgDelete.OFF)
    carts = relationship('Cart', back_populates='user')


# Class Cart
class Cart(Base):
    """
        Model cart
    """
    __tablename__ = 'cart'
    cart_id = Column(String(20), primary_key=True)
    name = Column(String(256))
    created_user = Column(String(256))
    created_date = Column(DateTime, default=func.now())
    updated_user = Column(String(256))
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    flg_del = Column(IntEnum(FlgDelete), default=FlgDelete.OFF)
    fk_user_id = Column(String(20), ForeignKey('user.user_id'))
    user = relationship('User', back_populates='carts')
    products = relationship('Product', back_populates='cart')

# Class Product
class Product(Base):
    """
        Model product
    """
    __tablename__ = 'product'
    product_id = Column(String(20), primary_key=True)
    name = Column(String(256), nullable=False)
    weight = Column(String(256))
    height = Column(String(256))
    qr_code = Column(String(256), nullable=False)
    created_user = Column(String(256))
    created_date = Column(DateTime, default=func.now())
    updated_user = Column(String(256))
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    flg_del = Column(IntEnum(FlgDelete), default=FlgDelete.OFF)
    fk_cart_id = Column(String(20), ForeignKey('cart.cart_id'))
    cart = relationship('Cart', back_populates='products')

class Post(Base):
    """
        Model post
    """
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(256))
    image_url_type = Column(String(256))
    caption = Column(String(1000))
    timestamp = Column(DateTime)
    created_user = Column(String(256))
    created_date = Column(DateTime, default=func.now())
    updated_user = Column(String(256))
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    flg_del = Column(IntEnum(FlgDelete), default=FlgDelete.OFF)

class Comment(Base):
    """
        Model comment
    """
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(1000))
    username = Column(String(256))
    timestamp = Column(DateTime)
    created_user = Column(String(256))
    created_date = Column(DateTime, default=func.now())
    updated_user = Column(String(256))
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    flg_del = Column(IntEnum(FlgDelete), default=FlgDelete.OFF)
