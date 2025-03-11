from post import PostRepository
from fastapi.encoders import jsonable_encoder
from core import CommonException

class PostService:
    """
        Post service
    """

    def __init__(self, post_repository: PostRepository):
        self.post_repo: PostRepository = post_repository

    def get_all(self):
        """
            # Get list post
            # Params:
            # Output:
            #   return: List of post
        """
        data = self.post_repo.get_all()
        return {"item": jsonable_encoder(data) if data else []}

    def get_by_post_id(self, post_id):
        """
            # Get post by post_id
            # Params:
            # @post_id: id of the post
            # Output:
            #   return: data post
        """
        data = self.post_repo.get_by_post_id(post_id)
        return jsonable_encoder(data) if data else None

    # Add post
    def add(self, data_request, created_user):
        """
            # Add post
            # Params:
            #   @data_request: data request
            #   @created_user: name of the add user
            # Output:
            #   return: Data post
        """
        # Handle save image
        self.post_repo.add(data_request, created_user)

    # Update post
    def update(self, post_id, data_request, updated_user):
        """
            # Update post
            # Params:
            #   @post_id: id of the post
            #   @data_request: data request
            #   @updated_user: name of the user
            # Output:
            #   return:
        """
        # Check if post already exists
        if not self.post_repo.get_by_post_id(post_id):
            raise CommonException(message="Post not exists")

        self.post_repo.update(post_id, data_request, updated_user)

    # Delete post
    def delete(self, post_id, updated_user):
        """
            # Update post
            # Params:
            #   @post_id: id of the post
            #   @updated_user: name of the user
            # Output:
            #   return:
        """
        # Check if post already exists
        if not self.post_repo.get_by_post_id(post_id):
            raise CommonException(message="Post not exists")
        self.post_repo.delete(post_id, updated_user)

    # Active post
    def active(self, post_id, updated_user):
        """
            # Active post
            # Params:
            #   @post_id: id of the post
            #   @updated_user: name of the user
            # Output:
            #   return:
        """
        # Check if post already exists
        if not self.post_repo.get_by_post_id(post_id):
            raise CommonException(message="Post not exists")
        self.post_repo.active(post_id, updated_user)
