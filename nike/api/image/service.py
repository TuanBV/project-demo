import base64
import os
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from core import CommonException
from image import ImageRepository

class ImageService:
    """
        Image service
    """

    def __init__(self, image_repository: ImageRepository):
        self.image_repo: ImageRepository = image_repository

    def get_all(self):
        """
            # Get list image
            # Params:
            # Output:
            #   return: List of image
        """
        data = self.image_repo.get_all()
        return {"item": jsonable_encoder(data) if data else []}

    # Add image
    def add(self, data_request, created_user):
        """
            # Add image
            # Params:
            #   @data_request: data request
            #   @created_user: name of the add user
            # Output:
            #   return: Data image
        """
        # Handle save image
        folder = "upload/images/"
        timestamp = int(datetime.now().timestamp())
        file_name = f'image_{timestamp}.{data_request["file_ext"]}'
        # Convert file data to base64
        image_image = base64.b64decode(data_request["file"])
        file_location = os.path.join(folder, file_name)
        with open(file_location, "wb") as file:
            file.write(image_image)
        data_request["name"] = file_name
        data_request["path"] = file_location

        return self.image_repo.add(data_request, created_user)

    # Delete image
    def delete(self, image_id, updated_user):
        """
            # Delete image
            # Params:
            #   @image_id: id of the image
            #   @updated_user: name of the user
            # Output:
            #   return:
        """
        # Check if image already exists
        if not self.image_repo.get_by_image_id(image_id):
            raise CommonException(message="Image not exists")
        self.image_repo.delete(image_id, updated_user)
