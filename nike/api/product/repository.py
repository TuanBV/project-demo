from models.model import Product
from utils.kbn import FlgDelete
from core import CommonRepository
from fastapi.encoders import jsonable_encoder
from sqlalchemy import asc, desc

class ProductRepository(CommonRepository):
    """
    Repository of product
    """

    def get_all(self):
        """
            # Get list product
            # Params:
            # Output:
            #   return: List of product
        """
        with self.session_factory_read() as session:
            return session.query(Product).order_by(
                asc(Product.flg_del), desc(Product.created_date)
            ).all()


    # Get user by user_id
    def get_by_product_id(self, product_id):
        """
            # Get product by product_id
            # Params:
            #   @product_id: Product id
            # Output:
            #   return: Data product
        """
        with self.session_factory_read() as session:
            return session.query(Product).filter(Product.id == product_id).first()

    # Add product
    def add(self, name, created_user):
        """
            # Add product
            # Params:
            #   @data: name
            # Output:
            #   return: data product
        """
        with self.session_factory() as session:
            new_product = Product(
                name=name,
                created_user=created_user
            )
            session.add(new_product)
            session.commit()
            session.refresh(new_product)

            return jsonable_encoder(new_product)

    # Get the product by name
    def get_by_name(self, name):
        """
            # Get the product by name
            # Params:
            #   @name: name of product
            # Output:
            #   return: Boolean
        """
        with self.session_factory_read() as session:
            return session.query(Product).filter(
                Product.name == name,
                Product.flg_del == FlgDelete.OFF.value
            ).first()

    # Update product
    def update(self, product_id, name, updated_user):
        """
            # Update product
            # Params:
            #   @product_id: id of the product
            #   @name: name of product
            #   @updated_user: name of user update
            # Output:
            #   return:
        """
        with self.session_factory() as session:
            session.query(Product).filter(
                Product.id == product_id,
                Product.flg_del == FlgDelete.OFF.value
            ).update({
                "name": name,
                "updated_user": updated_user
            })
            session.commit()

    # Delete product
    def delete(self, product_id, updated_user):
        """
            # Delete product
            # Params:
            #   @product_id: id of the product
            #   @updated_user: name of user update
            # Output:
            #   return:
        """
        with self.session_factory() as session:
            session.query(Product).filter(
                Product.id == product_id,
                Product.flg_del == FlgDelete.OFF.value
            ).update({
                "flg_del": FlgDelete.ON.value,
                "updated_user": updated_user
            })
            session.commit()

    # Active product
    def active(self, product_id, updated_user):
        """
            # Active product
            # Params:
            #   @product_id: id of the product
            #   @updated_user: name of user update
            # Output:
            #   return:
        """
        with self.session_factory() as session:
            session.query(Product).filter(
                Product.id == product_id
            ).update({
                "flg_del": FlgDelete.OFF.value,
                "updated_user": updated_user
            })
            session.commit()
