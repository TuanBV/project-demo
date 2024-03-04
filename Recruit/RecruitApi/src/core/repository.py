"""
Common repository
"""

from models import Candidates
from helpers import kbn


class CommonRepository():
  """
  Common of Repository
  """
  def __init__(self, session_factory, session_factory_read):
    self.session_factory = session_factory
    self.session_factory_read = session_factory_read


  # Get data candidate
  # Params:
  #   @candidate_id: Id candidate
  # Output:
  #  return: Data candidate
  def get_candidate(self, candidate_id):
    with self.session_factory_read() as session:
      result_candidate= session.query(Candidates).filter(Candidates.id == candidate_id,
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value).first()

      return result_candidate
