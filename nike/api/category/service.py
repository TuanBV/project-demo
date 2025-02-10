from category import CategoryRepository
from fastapi.encoders import jsonable_encoder
from core import CommonException

class CategoryService:
    """
        Category service
    """

    def __init__(self, category_repository: CategoryRepository):
        self.category_repo: CategoryRepository = category_repository

    def get_all(self):
        """
            # Get list category
            # Params:
            # Output:
            #   return: List of category
        """
        data = self.category_repo.get_all()
        return {"item": jsonable_encoder(data)}

    def get_by_category_id(self, category_id):
        """
            # Get category by category_id
            # Params:
            # @category_id: id of the category
            # Output:
            #   return: data category
        """
        data = self.category_repo.get_by_category_id(category_id)
        if data:
            return jsonable_encoder(data)


    # Add category
    def add(self, name, created_user):
        """
            # Add category
            # Params:
            #   @name: name of the category
            #   @created_user: name of the add user
            # Output:
            #   return: Data category
        """
        # Check if category already exists
        if self.category_repo.get_by_name(name):
            raise CommonException(message="Category name already exists")
        return self.category_repo.add(name, created_user)

    # Update category
    def update(self, category_id, name, updated_user):
        """
            # Update category
            # Params:
            #   @category_id: id of the category
            #   @name: name of the category
            #   @updated_user: name of the user
            # Output:
            #   return:
        """
        # Check if category already exists
        if not self.category_repo.get_by_category_id(category_id):
            raise CommonException(message="Category not exists")
        if self.category_repo.get_by_name(name):
            raise CommonException(message="Category name exists")
        self.category_repo.update(category_id, name, updated_user)

    # Delete category
    def delete(self, category_id, updated_user):
        """
            # Update category
            # Params:
            #   @category_id: id of the category
            #   @updated_user: name of the user
            # Output:
            #   return:
        """
        # Check if category already exists
        if not self.category_repo.get_by_category_id(category_id):
            raise CommonException(message="Category not exists")
        self.category_repo.delete(category_id, updated_user)

    # Active category
    def active(self, category_id, updated_user):
        """
            # Active category
            # Params:
            #   @category_id: id of the category
            #   @updated_user: name of the user
            # Output:
            #   return:
        """
        # Check if category already exists
        if elf.category_repo.get_by_category_id(category_id):
            raise CommonException(message="Category not exists")
        self.category_repo.active(category_id, updated_user)
