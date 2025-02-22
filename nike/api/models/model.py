from db.database import Base
from utils.kbn import IntEnum, FlgDelete, ROLE
from sqlalchemy import Column, Integer, String, DateTime, func, Index, Double, Date
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
    user_id = Column(String(20), ForeignKey('user.user_id'))
    user = relationship('User', back_populates='carts')

    cart_products = relationship("CartProduct", back_populates="cart")

# Category
class Category(Base):
    """
        Model category
    """
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    created_user = Column(String(256))
    created_date = Column(DateTime, default=func.now())
    updated_user = Column(String(256))
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    flg_del = Column(IntEnum(FlgDelete), default=FlgDelete.OFF)

    products = relationship('Product', back_populates='category')

class Sale(Base):
    """
        Model sale
    """
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    discount = Column(Integer, nullable=False)
    image = Column(String(256))
    start_date = Column(Date)
    end_date = Column(Date)
    created_user = Column(String(256))
    created_date = Column(DateTime, default=func.now())
    updated_user = Column(String(256))
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    flg_del = Column(IntEnum(FlgDelete), default=FlgDelete.OFF)

    products = relationship('Product', back_populates='sale')

# Class Product
class Product(Base):
    """
        Model product
    """
    __tablename__ = 'product'
    product_id = Column(String(20), primary_key=True)
    name = Column(String(256), nullable=False)
    quantity = Column(Integer, default=0)
    price = Column(Double, default=0)
    weight = Column(String(256))
    height = Column(String(256))
    created_user = Column(String(256))
    created_date = Column(DateTime, default=func.now())
    updated_user = Column(String(256))
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    flg_del = Column(IntEnum(FlgDelete), default=FlgDelete.OFF)
    # Foreign key
    category_id = Column(Integer, ForeignKey('category.id'))
    sale_id = Column(Integer, ForeignKey('sale.id'))
    sale = relationship('Sale', back_populates='products')
    category = relationship('Category', back_populates='products')
    product_image = relationship('ProductImage', back_populates='products')

    cart_products = relationship("CartProduct", back_populates="products")

class ProductImage(Base):
    """
        Model product_image
    """
    __tablename__ = 'product_image'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(256))
    name = Column(String(256))
    created_user = Column(String(256))
    created_date = Column(DateTime, default=func.now())
    updated_user = Column(String(256))
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    flg_del = Column(IntEnum(FlgDelete), default=FlgDelete.OFF)

    product_id = Column(String(20), ForeignKey("product.product_id"))
    products = relationship('Product', back_populates='product_image')

class Image(Base):
    """
        Model image
    """
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    path = Column(String(256), nullable=False)
    created_user = Column(String(256))
    created_date = Column(DateTime, default=func.now())
    updated_user = Column(String(256))
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    flg_del = Column(IntEnum(FlgDelete), default=FlgDelete.OFF)


class CartProduct(Base):
    """
        Model cart_product
    """
    __tablename__ = 'cart_product'

    cart_id = Column(Integer, ForeignKey('cart.cart_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.product_id'), primary_key=True)
    quantity = Column(Integer)

    cart = relationship("Cart", back_populates="cart_products")
    products = relationship("Product", back_populates="cart_products")

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

class Offer(Base):
    """
        Model offer
    """
    __tablename__ = 'offer'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String(256), nullable=False, unique=True)
    created_user = Column(String(256))
    created_date = Column(DateTime, default=func.now())
    updated_user = Column(String(256))
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    flg_del = Column(IntEnum(FlgDelete), default=FlgDelete.OFF)
    __table_args__ = (
        Index('index_offer_email', 'email'),
    )
