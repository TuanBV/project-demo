# import base64
# import os
from fastapi.encoders import jsonable_encoder
from setting import SettingRepository
from core import CommonException

class SettingService:
    """
        Setting service
    """

    def __init__(self, setting_repository: SettingRepository):
        self.setting_repo: SettingRepository = setting_repository

    def get_all(self):
        """
            # Get setting list
            # Params:
            # Output:
            #   return: Setting list
        """
        data = self.setting_repo.get_all()
        return {"item": jsonable_encoder(data)}

    def get_new_setting(self):
        """
            # Get new setting
            # Params:
            # Output:
            #   return: new setting
        """
        data = self.setting_repo.get_new_setting()
        return jsonable_encoder(data)

    # Save setting info about company
    def save(self, data_request, created_user):
        """
            # Save setting info about company
            # Params:
            #   @data_request: data request
            #   @created_user: name of the add user
            # Output:
            #   return: Data setting
        """
        return self.setting_repo.save(data_request, created_user)
