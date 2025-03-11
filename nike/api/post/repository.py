from models.model import Post
from utils.kbn import FlgDelete
from core import CommonRepository
from fastapi.encoders import jsonable_encoder
from sqlalchemy import asc, desc
import datetime
class PostRepository(CommonRepository):
    """
    Repository of post
    """

    def get_all(self):
        """
            # Get list post
            # Params:
            # Output:
            #   return: List of post
        """
        with self.session_factory_read() as session:
            return session.query(Post).order_by(
                asc(Post.flg_del), asc(Post.start_date), asc(Post.title),
            ).all()


    # Get user by user_id
    def get_by_post_id(self, post_id):
        """
            # Get post by post_id
            # Params:
            #   @post_id: Post id
            # Output:
            #   return: Data post
        """
        with self.session_factory_read() as session:
            return session.query(Post).filter(Post.id == post_id).first()

    # Add post
    def add(self, data_request, created_user):
        """
            # Add post
            # Params:
            #   @data_request: data request
            #   @created_user: name of the created user
            # Output:
            #   return: data post
        """
        with self.session_factory() as session:
            # Add post
            new_post = Post(
                title=data_request['title'],
                content=data_request['content'],
                start_date=data_request['start_date'] if data_request['start_date'] else None,
                created_user=created_user
            )
            session.add(new_post)
            session.commit()
            session.refresh(new_post)

    # Get the post by name
    def get_by_name(self, name):
        """
            # Get the post by name
            # Params:
            #   @name: name of post
            # Output:
            #   return: Boolean
        """
        with self.session_factory_read() as session:
            return session.query(Post).filter(
                Post.name == name,
                Post.flg_del == FlgDelete.OFF.value
            ).first()

    # Update post
    def update(self, post_id, data_request, updated_user):
        """
            # Update post
            # Params:
            #   @post_id: id of the post
            #   @data_request: data_request
            #   @updated_user: name of user update
            # Output:
            #   return:
        """
        with self.session_factory() as session:
            session.query(Post).filter(
                Post.id == post_id,
                Post.flg_del == FlgDelete.OFF.value
            ).update({
                "name": data_request["name"],
                "discount": data_request["discount"],
                "start_date": data_request["start_date"] if data_request["start_date"] else None,
                "end_date": data_request["end_date"] if data_request["end_date"] else None,
                "updated_user": updated_user
            })
            session.commit()

    # Delete post
    def delete(self, post_id, updated_user):
        """
            # Delete post
            # Params:
            #   @post_id: id of the post
            #   @updated_user: name of user update
            # Output:
            #   return:
        """
        with self.session_factory() as session:
            session.query(Post).filter(
                Post.id == post_id,
                Post.flg_del == FlgDelete.OFF.value
            ).update({
                "flg_del": FlgDelete.ON.value,
                "updated_user": updated_user
            })
            session.commit()

    # Active post
    def active(self, post_id, updated_user):
        """
            # Active post
            # Params:
            #   @post_id: id of the post
            #   @updated_user: name of user update
            # Output:
            #   return:
        """
        with self.session_factory() as session:
            session.query(Post).filter(
                Post.id == post_id
            ).update({
                "flg_del": FlgDelete.OFF.value,
                "updated_user": updated_user
            })
            session.commit()
