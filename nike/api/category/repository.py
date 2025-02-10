from models.model import Category
from utils.kbn import FlgDelete
from core import CommonRepository
from fastapi.encoders import jsonable_encoder
from sqlalchemy import asc, desc

class CategoryRepository(CommonRepository):
    """
    Repository of category
    """

    def get_all(self):
        """
            # Get list category
            # Params:
            # Output:
            #   return: List of category
        """
        with self.session_factory_read() as session:
            return session.query(Category).order_by(
                asc(Category.flg_del), desc(Category.created_date)
            ).all()


    # Get user by user_id
    def get_by_category_id(self, category_id):
        """
            # Get category by category_id
            # Params:
            #   @category_id: Category id
            # Output:
            #   return: Data category
        """
        with self.session_factory_read() as session:
            return session.query(Category).filter(Category.id == category_id).first()

    # Add category
    def add(self, name, created_user):
        """
            # Add category
            # Params:
            #   @data: name
            # Output:
            #   return: data category
        """
        with self.session_factory() as session:
            new_category = Category(
                name=name,
                created_user=created_user
            )
            session.add(new_category)
            session.commit()
            session.refresh(new_category)

            return jsonable_encoder(new_category)

    # Get the category by name
    def get_by_name(self, name):
        """
            # Get the category by name
            # Params:
            #   @name: name of category
            # Output:
            #   return: Boolean
        """
        with self.session_factory_read() as session:
            return session.query(Category).filter(
                Category.name == name,
                Category.flg_del == FlgDelete.OFF.value
            ).first()

    # Update category
    def update(self, category_id, name, updated_user):
        """
            # Update category
            # Params:
            #   @category_id: id of the category
            #   @name: name of category
            #   @updated_user: name of user update
            # Output:
            #   return:
        """
        with self.session_factory() as session:
            session.query(Category).filter(
                Category.id == category_id,
                Category.flg_del == FlgDelete.OFF.value
            ).update({
                "name": name,
                "updated_user": updated_user
            })
            session.commit()

    # Delete category
    def delete(self, category_id, updated_user):
        """
            # Delete category
            # Params:
            #   @category_id: id of the category
            #   @updated_user: name of user update
            # Output:
            #   return:
        """
        with self.session_factory() as session:
            session.query(Category).filter(
                Category.id == category_id,
                Category.flg_del == FlgDelete.OFF.value
            ).update({
                "flg_del": FlgDelete.ON.value,
                "updated_user": updated_user
            })
            session.commit()

    # Active category
    def active(self, category_id, updated_user):
        """
            # Active category
            # Params:
            #   @category_id: id of the category
            #   @updated_user: name of user update
            # Output:
            #   return:
        """
        with self.session_factory() as session:
            session.query(Category).filter(
                Category.id == category_id
            ).update({
                "flg_del": FlgDelete.OFF.value,
                "updated_user": updated_user
            })
            session.commit()
