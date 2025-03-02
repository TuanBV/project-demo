from product import ProductRepository
from sale import SaleRepository
from image import ImageRepository
from category import CategoryRepository
from fastapi.encoders import jsonable_encoder
from core import CommonException

class ProductService:
    """
        Product service
    """

    def __init__(self, product_repository: ProductRepository,
                sale_repository: SaleRepository,
                image_repository: ImageRepository,
                category_repository: CategoryRepository):
        self.product_repo: ProductRepository = product_repository
        self.sale_repo: SaleRepository = sale_repository
        self.image_repo: ImageRepository = image_repository
        self.category_repo: CategoryRepository = category_repository

    def get_all(self):
        """
            # Get list product
            # Params:
            # Output:
            #   return: List of product
        """
        data = self.product_repo.get_all()
        return {"item": jsonable_encoder(data)}

    def get_by_product_id(self, product_id):
        """
            # Get product by product_id
            # Params:
            # @product_id: id of the product
            # Output:
            #   return: data product
        """
        data = self.product_repo.get_by_product_id(product_id)
        if data:
            return jsonable_encoder(data)

    # Add product
    def add(self, data_request, created_user):
        """
            # Add product
            # Params:
            #   @data_request: data of request
            #   @created_user: name of the add user
            # Output:
            #   return: Data product
        """
        # Check image of data request
        if data_request["images"] \
            and len(data_request["images"])!= self.product_repo.count(data_request["images"]):
            raise CommonException(message="Image not exists")
        # Check category and kind of product in ProductKind table
        product_kind = self.product_repo.get_product_kind(
            data_request["category_id"], data_request["kind_id"]
        )
        data_request["product_kind_id"] = self.product_repo.add_product_kind(
                data_request["category_id"], data_request["kind_id"], created_user
            ) if not product_kind else product_kind.id

        self.product_repo.add(data_request, created_user)

    # Update product
    def update(self, product_id, name, updated_user):
        """
            # Update product
            # Params:
            #   @product_id: id of the product
            #   @name: name of the product
            #   @updated_user: name of the user
            # Output:
            #   return:
        """
        # Check if product already exists
        if not self.product_repo.get_by_product_id(product_id):
            raise CommonException(message="Product not exists")
        if self.product_repo.get_by_name(name):
            raise CommonException(message="Product name exists")
        self.product_repo.update(product_id, name, updated_user)

    # Delete product
    def delete(self, product_id, updated_user):
        """
            # Update product
            # Params:
            #   @product_id: id of the product
            #   @updated_user: name of the user
            # Output:
            #   return:
        """
        # Check if product already exists
        if not self.product_repo.get_by_product_id(product_id):
            raise CommonException(message="Product not exists")
        self.product_repo.delete(product_id, updated_user)

    # Active product
    def active(self, product_id, updated_user):
        """
            # Active product
            # Params:
            #   @product_id: id of the product
            #   @updated_user: name of the user
            # Output:
            #   return:
        """
        # Check if product already exists
        if not self.product_repo.get_by_product_id(product_id):
            raise CommonException(message="Product not exists")
        self.product_repo.active(product_id, updated_user)
