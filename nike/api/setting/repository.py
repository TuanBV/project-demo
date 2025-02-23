from models.model import Setting
from core import CommonRepository
from fastapi.encoders import jsonable_encoder

class SettingRepository(CommonRepository):
    """
    Repository of setting
    """

    # Get setting list
    def get_all(self):
        """
            # Get setting list
            # Params:
            # Output:
            #   return: Setting list
        """
        with self.session_factory_read() as session:
            return session.query(Setting).all()

    # Get new setting
    def get_new_setting(self):
        """
            # Get new setting
            # Params:
            # Output:
            #   return: New setting
        """
        with self.session_factory_read() as session:
            return session.query(Setting).order_by(Setting.id.desc()).first()


    # Save setting info about company
    def save(self, data_request, created_user):
        """
            # Save setting info about company
            # Params:
            #   @data_request: data request
            #   @created_user: name of the created user
            # Output:
            #   return: data setting
        """
        with self.session_factory() as session:
            new_setting = Setting(
                email=data_request['email'],
                number_phone=data_request['number_phone'],
                address=data_request['address'],
                info=data_request['info'],
                fb_link=data_request['fb_link'],
                ig_link=data_request['ig_link'],
                tt_link=data_request['tt_link'],
                tw_link=data_request['tw_link'],
                created_user=created_user
            )
            session.add(new_setting)
            session.commit()
            session.refresh(new_setting)
            return jsonable_encoder(new_setting)
