from models.model import Kind
from utils.kbn import FlgDelete
from core import CommonRepository
from fastapi.encoders import jsonable_encoder
from sqlalchemy import asc, desc

class KindRepository(CommonRepository):
    """
    Repository of kind
    """

    def get_all(self):
        """
            # Get list kind
            # Params:
            # Output:
            #   return: List of kind
        """
        with self.session_factory_read() as session:
            return session.query(Kind).order_by(
                asc(Kind.flg_del), desc(Kind.created_date)
            ).all()


    # Get user by user_id
    def get_by_kind_id(self, kind_id):
        """
            # Get kind by kind_id
            # Params:
            #   @kind_id: Kind id
            # Output:
            #   return: Data kind
        """
        with self.session_factory_read() as session:
            return session.query(Kind).filter(Kind.id == kind_id).first()

    # Add kind
    def add(self, name, created_user):
        """
            # Add kind
            # Params:
            #   @data: name
            # Output:
            #   return: data kind
        """
        with self.session_factory() as session:
            new_kind = Kind(
                name=name,
                created_user=created_user
            )
            session.add(new_kind)
            session.commit()
            session.refresh(new_kind)

            return jsonable_encoder(new_kind)

    # Get the kind by name
    def get_by_name(self, name):
        """
            # Get the kind by name
            # Params:
            #   @name: name of kind
            # Output:
            #   return: Boolean
        """
        with self.session_factory_read() as session:
            return session.query(Kind).filter(
                Kind.name == name,
                Kind.flg_del == FlgDelete.OFF.value
            ).first()

    # Update kind
    def update(self, kind_id, name, updated_user):
        """
            # Update kind
            # Params:
            #   @kind_id: id of the kind
            #   @name: name of kind
            #   @updated_user: name of user update
            # Output:
            #   return:
        """
        with self.session_factory() as session:
            session.query(Kind).filter(
                Kind.id == kind_id,
                Kind.flg_del == FlgDelete.OFF.value
            ).update({
                "name": name,
                "updated_user": updated_user
            })
            session.commit()

    # Delete kind
    def delete(self, kind_id, updated_user):
        """
            # Delete kind
            # Params:
            #   @kind_id: id of the kind
            #   @updated_user: name of user update
            # Output:
            #   return:
        """
        with self.session_factory() as session:
            session.query(Kind).filter(
                Kind.id == kind_id,
                Kind.flg_del == FlgDelete.OFF.value
            ).update({
                "flg_del": FlgDelete.ON.value,
                "updated_user": updated_user
            })
            session.commit()

    # Active kind
    def active(self, kind_id, updated_user):
        """
            # Active kind
            # Params:
            #   @kind_id: id of the kind
            #   @updated_user: name of user update
            # Output:
            #   return:
        """
        with self.session_factory() as session:
            session.query(Kind).filter(
                Kind.id == kind_id
            ).update({
                "flg_del": FlgDelete.OFF.value,
                "updated_user": updated_user
            })
            session.commit()
