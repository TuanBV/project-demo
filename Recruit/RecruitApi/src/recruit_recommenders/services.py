"""
Recommenders Service
"""
from recruit_recommenders import RecommendersRepository
from core import CommonException, ERR_MESSAGE
from fastapi.encoders import jsonable_encoder


class RecommendersService:
  """
    Recommenders service
  """
  def __init__(self, recommenders_repository: RecommendersRepository):
    self.recommenders_repo: RecommendersRepository = recommenders_repository


  # Get list action detail function
  # Output:
  #  return: List action detail
  def get_list(self):
    # Get list action
    payload = self.recommenders_repo.get_list()
    return payload


  # Add recommenders
  # Params:
  #   @data: Data request
  # Output:
  #   return: Recommender
  def add(self, data):
    flag_email_exist = self.recommenders_repo.check_recommenders_email_exist(data["recommender"]["email"])

    # Check email exist
    if flag_email_exist:
      raise CommonException(message=ERR_MESSAGE.EMAIL_EXIST)

    flag_telephone_exist = self.recommenders_repo.check_recommenders_telephone_exist(data["recommender"]["telephone_no"])

    # Check telephone exist
    if flag_telephone_exist:
      raise CommonException(message=ERR_MESSAGE.TEL_EXIST)

    flag_ident_number = self.recommenders_repo.check_recommenders_ident_number(data["recommender"]["identification_number"])

    # Check ident number exist
    if flag_ident_number:
      raise CommonException(message=ERR_MESSAGE.IDENT_EXIST)

    return self.recommenders_repo.add(data)


  # Get recommender
  # Params:
  #   @recommender_id: Recommender id
  # Output:
  #   return: Data recommender
  def get_recommender(self, recommender_id):
    result_recommender = jsonable_encoder(self.recommenders_repo.get_recommender_by_id(recommender_id))

    # Recommender not exist
    if not result_recommender:
      raise CommonException(message=ERR_MESSAGE.RECOMMENDER_NOT_EXIST)

    return result_recommender


  # Edit recommender
  # Params:
  #   @data: Data request
  # Output:
  #   return: Void
  def edit(self, data):
    result_recommender = self.recommenders_repo.get_recommender_by_id(data["recommender_id"])

    # Recommender not exist
    if not result_recommender:
      raise CommonException(message=ERR_MESSAGE.RECOMMENDER_NOT_EXIST)

    # Check current email is different from the email request
    if result_recommender.email != data["recommender"]["email"]:
      flag_email_exist = self.recommenders_repo.check_recommenders_email_exist(data["recommender"]["email"])

      # Check email exist
      if flag_email_exist:
        raise CommonException(message=ERR_MESSAGE.EMAIL_EXIST)

    # Check current telephone is different from the telephone request
    if result_recommender.telephone_no != data["recommender"]["telephone_no"]:
      flag_telephone_exist = self.recommenders_repo.check_recommenders_telephone_exist(data["recommender"]["telephone_no"])

      # Check telephone exist
      if flag_telephone_exist:
        raise CommonException(message=ERR_MESSAGE.TEL_EXIST)

    # Check current identification_number is different from the identification_number request
    if result_recommender.identification_number != data["recommender"]["identification_number"]:
      flag_ident_number = self.recommenders_repo.check_recommenders_ident_number(data["recommender"]["identification_number"])

      # Check ident number exist
      if flag_ident_number:
        raise CommonException(message=ERR_MESSAGE.IDENT_NUMBER_EXIST)

    self.recommenders_repo.edit(data)


  # Delete recommenders
  # Param:
  #   @data: Data request
  # Output:
  #   return: Void
  def delete(self, data):
    result_recommender = self.recommenders_repo.get_recommender_by_id(data["recommender_id"])

    # Recommender not exist
    if not result_recommender:
      raise CommonException(message=ERR_MESSAGE.RECOMMENDER_NOT_EXIST)

    self.recommenders_repo.delete(data)
