from models.model import Image, ProductImage
from core import CommonRepository
from fastapi.encoders import jsonable_encoder
from utils.kbn import FlgDelete

class ImageRepository(CommonRepository):
    """
    Repository of image
    """

    def get_all(self):
        """
            # Get list image
            # Params:
            # Output:
            #   return: List of image
        """
        with self.session_factory_read() as session:
            return session.query(Image).filter(
                Image.flg_del == FlgDelete.OFF.value
            ).all()

    # Get image by image_id
    def get_by_image_id(self, image_id):
        """
            # Get image by image_id
            # Params:
            #   @image_id: Image id
            # Output:
            #   return: Data image
        """
        with self.session_factory_read() as session:
            return session.query(Image).filter(
                Image.id == image_id,
                Image.flg_del == FlgDelete.OFF.value
            ).first()


    # Add image
    def add(self, data_request, created_user):
        """
            # Add image
            # Params:
            #   @data_request: data request
            #   @created_user: name of the created user
            # Output:
            #   return: data image
        """
        with self.session_factory() as session:
            new_image = Image(
                name=data_request['name'],
                path=data_request['path'],
                created_user=created_user
            )
            session.add(new_image)
            session.commit()
            session.refresh(new_image)
            return jsonable_encoder(new_image)

    # Delete image
    def delete(self, image_id, updated_user):
        """
            # Delete image
            # Params:
            #   @image_id: id of the image
            #   @updated_user: name of user update
            # Output:
            #   return:
        """
        with self.session_factory() as session:
            session.query(Image).filter(
                Image.id == image_id,
                Image.flg_del == FlgDelete.OFF.value
            ).update({
                "flg_del": FlgDelete.ON.value,
                "updated_user": updated_user
            })
            session.commit()
