from kind import KindRepository
from fastapi.encoders import jsonable_encoder
from core import CommonException

class KindService:
    """
        Kind service
    """

    def __init__(self, kind_repository: KindRepository):
        self.kind_repo: KindRepository = kind_repository

    def get_all(self):
        """
            # Get list kind
            # Params:
            # Output:
            #   return: List of kind
        """
        data = self.kind_repo.get_all()
        return {"item": jsonable_encoder(data)}

    def get_by_kind_id(self, kind_id):
        """
            # Get kind by kind_id
            # Params:
            # @kind_id: id of the kind
            # Output:
            #   return: data kind
        """
        data = self.kind_repo.get_by_kind_id(kind_id)
        if data:
            return jsonable_encoder(data)


    # Add kind
    def add(self, name, created_user):
        """
            # Add kind
            # Params:
            #   @name: name of the kind
            #   @created_user: name of the add user
            # Output:
            #   return: Data kind
        """
        # Check if kind already exists
        if self.kind_repo.get_by_name(name):
            raise CommonException(message="Kind name already exists")
        return self.kind_repo.add(name, created_user)

    # Update kind
    def update(self, kind_id, name, updated_user):
        """
            # Update kind
            # Params:
            #   @kind_id: id of the kind
            #   @name: name of the kind
            #   @updated_user: name of the user
            # Output:
            #   return:
        """
        # Check if kind already exists
        if not self.kind_repo.get_by_kind_id(kind_id):
            raise CommonException(message="Kind not exists")
        if self.kind_repo.get_by_name(name):
            raise CommonException(message="Kind name exists")
        self.kind_repo.update(kind_id, name, updated_user)

    # Delete kind
    def delete(self, kind_id, updated_user):
        """
            # Update kind
            # Params:
            #   @kind_id: id of the kind
            #   @updated_user: name of the user
            # Output:
            #   return:
        """
        # Check if kind already exists
        if not self.kind_repo.get_by_kind_id(kind_id):
            raise CommonException(message="Kind not exists")
        self.kind_repo.delete(kind_id, updated_user)

    # Active kind
    def active(self, kind_id, updated_user):
        """
            # Active kind
            # Params:
            #   @kind_id: id of the kind
            #   @updated_user: name of the user
            # Output:
            #   return:
        """
        # Check if kind already exists
        if not self.kind_repo.get_by_kind_id(kind_id):
            raise CommonException(message="Kind not exists")
        self.kind_repo.active(kind_id, updated_user)
