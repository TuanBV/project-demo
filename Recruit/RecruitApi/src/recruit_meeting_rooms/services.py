"""
Meeting rooms Service
"""
from recruit_meeting_rooms import MeetingRoomsRepository
from fastapi.encoders import jsonable_encoder


class MeetingRoomsService:
  """
    Meeting rooms service
  """
  def __init__(self, meeting_rooms_repository: MeetingRoomsRepository):
    self.meeting_rooms_repo: MeetingRoomsRepository = meeting_rooms_repository

  # List meeting room
  # Param: None
  # Return: None
  def get_list(self):
    data_rooms = self.meeting_rooms_repo.get_list()

    return {
      "item": jsonable_encoder(data_rooms),
    }
