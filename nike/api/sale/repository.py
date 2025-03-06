from models.model import Sale, Image
from utils.kbn import FlgDelete
from core import CommonRepository
from fastapi.encoders import jsonable_encoder
from sqlalchemy import asc, desc, outerjoin
from helpers.const import IMAGE_FOLDER
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
            results = session.query(Sale, Image).outerjoin(
                Image, Image.id == Sale.image_id
            ).order_by(
                asc(Sale.flg_del), desc(Sale.end_date),
                desc(Sale.start_date), desc(Sale.discount),
                asc(Sale.name), desc(Sale.created_date)
            ).all()

            # Format json to data
            return [
                {
                    "id": sale.id,
                    "name": sale.name,
                    "discount": sale.discount,
                    "image": image.path if image else None,
                    "start_date": jsonable_encoder(sale.start_date),
                    "end_date": jsonable_encoder(sale.end_date),
                    "flg_del": jsonable_encoder(sale.flg_del),

                } for sale, image in results
            ]

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
            # Add image
            image = Image(
                name=data_request['name'],
                path=data_request['path'],
                folder=IMAGE_FOLDER.SALE
            )
            session.add(image)
            session.flush()
            # Add sale
            new_sale = Sale(
                name=data_request['name'],
                discount=data_request['discount'],
                image_id=image.id,
                start_date=data_request['start_date'] if data_request['start_date'] else None,
                end_date=data_request['end_date'] if data_request['end_date'] else None,
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
    def update(self, sale_id, data_request, updated_user):
        """
            # Update sale
            # Params:
            #   @sale_id: id of the sale
            #   @data_request: data_request
            #   @updated_user: name of user update
            # Output:
            #   return:
        """
        with self.session_factory() as session:
            session.query(Sale).filter(
                Sale.id == sale_id,
                Sale.flg_del == FlgDelete.OFF.value
            ).update({
                "name": data_request["name"],
                "discount": data_request["discount"],
                "start_date": data_request["start_date"] if data_request["start_date"] else None,
                "end_date": data_request["end_date"] if data_request["end_date"] else None,
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
