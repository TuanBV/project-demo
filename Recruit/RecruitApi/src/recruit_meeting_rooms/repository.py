"""
Meeting rooms repository
"""

from core import CommonRepository
from models import MeetingRooms
from helpers import kbn

class MeetingRoomsRepository(CommonRepository):
  """
  Repository of Service meeting room
  """

  # Get list meeting room
  # Params:
  # Output:
  #   return: list meeting room
  def get_list(self):
    with self.session_factory_read() as session:
      return session.query(MeetingRooms).filter(MeetingRooms.is_deleted == kbn.DeleteFlag.OFF.value).all()


  # Get meeting room by id
  # Params:
  #   @room_id: Id room
  # Output:
  #   return: Meeting room
  def get_room_by_id(self, room_id):
    with self.session_factory_read() as session:
      return session.query(MeetingRooms).filter(MeetingRooms.id == room_id, MeetingRooms.is_deleted == kbn.DeleteFlag.OFF.value).first()
