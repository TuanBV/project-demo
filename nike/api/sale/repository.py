from models.model import Sale
from utils.kbn import FlgDelete
from core import CommonRepository
from fastapi.encoders import jsonable_encoder
from sqlalchemy import asc, desc

class SaleRepository(CommonRepository):
    """
    Repository of sale
    """

    def get_all(self):
        """
            # Get list sale
            # Params:
            # Output:
            #   return: List of sale
        """
        with self.session_factory_read() as session:
            return session.query(Sale).order_by(
                asc(Sale.flg_del), desc(Sale.end_date),
                desc(Sale.start_date), desc(Sale.discount),
                asc(Sale.name), desc(Sale.created_date)
            ).all()


    # Get user by user_id
    def get_by_sale_id(self, sale_id):
        """
            # Get sale by sale_id
            # Params:
            #   @sale_id: Sale id
            # Output:
            #   return: Data sale
        """
        with self.session_factory_read() as session:
            return session.query(Sale).filter(Sale.id == sale_id).first()

    # Add sale
    def add(self, data_request, created_user):
        """
            # Add sale
            # Params:
            #   @data_request: data request
            #   @created_user: name of the created user
            # Output:
            #   return: data sale
        """
        with self.session_factory() as session:
            new_sale = Sale(
                name=data_request['name'],
                discount=data_request['discount'],
                start_date=data_request['start_date'],
                end_date=data_request['end_date'],
                created_user=created_user
            )
            session.add(new_sale)
            session.commit()
            session.refresh(new_sale)

            return jsonable_encoder(new_sale)

    # Get the sale by name
    def get_by_name(self, name):
        """
            # Get the sale by name
            # Params:
            #   @name: name of sale
            # Output:
            #   return: Boolean
        """
        with self.session_factory_read() as session:
            return session.query(Sale).filter(
                Sale.name == name,
                Sale.flg_del == FlgDelete.OFF.value
            ).first()

    # Update sale
    def update(self, sale_id, name, updated_user):
        """
            # Update sale
            # Params:
            #   @sale_id: id of the sale
            #   @name: name of sale
            #   @updated_user: name of user update
            # Output:
            #   return:
        """
        with self.session_factory() as session:
            session.query(Sale).filter(
                Sale.id == sale_id,
                Sale.flg_del == FlgDelete.OFF.value
            ).update({
                "name": name,
                "updated_user": updated_user
            })
            session.commit()

    # Delete sale
    def delete(self, sale_id, updated_user):
        """
            # Delete sale
            # Params:
            #   @sale_id: id of the sale
            #   @updated_user: name of user update
            # Output:
            #   return:
        """
        with self.session_factory() as session:
            session.query(Sale).filter(
                Sale.id == sale_id,
                Sale.flg_del == FlgDelete.OFF.value
            ).update({
                "flg_del": FlgDelete.ON.value,
                "updated_user": updated_user
            })
            session.commit()

    # Active sale
    def active(self, sale_id, updated_user):
        """
            # Active sale
            # Params:
            #   @sale_id: id of the sale
            #   @updated_user: name of user update
            # Output:
            #   return:
        """
        with self.session_factory() as session:
            session.query(Sale).filter(
                Sale.id == sale_id
            ).update({
                "flg_del": FlgDelete.OFF.value,
                "updated_user": updated_user
            })
            session.commit()
