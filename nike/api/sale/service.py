from sale import SaleRepository
from fastapi.encoders import jsonable_encoder
from core import CommonException

class SaleService:
    """
        Sale service
    """

    def __init__(self, sale_repository: SaleRepository):
        self.sale_repo: SaleRepository = sale_repository

    def get_all(self):
        """
            # Get list sale
            # Params:
            # Output:
            #   return: List of sale
        """
        data = self.sale_repo.get_all()
        return {"item": jsonable_encoder(data)}

    def get_by_sale_id(self, sale_id):
        """
            # Get sale by sale_id
            # Params:
            # @sale_id: id of the sale
            # Output:
            #   return: data sale
        """
        data = self.sale_repo.get_by_sale_id(sale_id)
        if data:
            return jsonable_encoder(data)


    # Add sale
    def add(self, data_request, created_user):
        """
            # Add sale
            # Params:
            #   @data_request: data request
            #   @created_user: name of the add user
            # Output:
            #   return: Data sale
        """
        # # Check if sale already exists
        # if self.sale_repo.get_by_name(name):
        #     raise CommonException(message="Sale name already exists")
        return self.sale_repo.add(data_request, created_user)

    # Update sale
    def update(self, sale_id, name, updated_user):
        """
            # Update sale
            # Params:
            #   @sale_id: id of the sale
            #   @name: name of the sale
            #   @updated_user: name of the user
            # Output:
            #   return:
        """
        # Check if sale already exists
        if not self.sale_repo.get_by_sale_id(sale_id):
            raise CommonException(message="Sale not exists")
        if self.sale_repo.get_by_name(name):
            raise CommonException(message="Sale name exists")
        self.sale_repo.update(sale_id, name, updated_user)

    # Delete sale
    def delete(self, sale_id, updated_user):
        """
            # Update sale
            # Params:
            #   @sale_id: id of the sale
            #   @updated_user: name of the user
            # Output:
            #   return:
        """
        # Check if sale already exists
        if not self.sale_repo.get_by_sale_id(sale_id):
            raise CommonException(message="Sale not exists")
        self.sale_repo.delete(sale_id, updated_user)

    # Active sale
    def active(self, sale_id, updated_user):
        """
            # Active sale
            # Params:
            #   @sale_id: id of the sale
            #   @updated_user: name of the user
            # Output:
            #   return:
        """
        # Check if sale already exists
        if not self.sale_repo.get_by_sale_id(sale_id):
            raise CommonException(message="Sale not exists")
        self.sale_repo.active(sale_id, updated_user)
