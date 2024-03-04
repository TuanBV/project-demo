"""
Parameter Service
"""
from core import CommonException, ERR_MESSAGE
from recruit_parameters import ParametersRepository
from fastapi.encoders import jsonable_encoder


class ParametersService:
  """
    Parameter service
  """
  def __init__(self, parameters_repository: ParametersRepository):
    self.parameters_repo: ParametersRepository = parameters_repository


  # Get list param
  # Param:
  #   @id_param: id of parameter
  # Return: list item parameter
  def get_list(self):
    list_parameter = self.parameters_repo.get_list()
    # Check param exist
    if not list_parameter:
      raise CommonException(message=ERR_MESSAGE.MSG_0005)

    return list_parameter


  # Get parameter by id
  # Param:
  #   @id_param: id of parameter
  # Return: item parameter
  def get_by_id(self, id_param):
    param = self.parameters_repo.get_by_id(id_param)
    # Check param exist
    if not param:
      raise CommonException(message=ERR_MESSAGE.MSG_0005)

    return jsonable_encoder(param)


  # Add parameter new
  # Param:
  #   @data_parameter: data request
  # Return: None
  def add(self, data_parameter):
    # Add parameter
    return self.parameters_repo.add(data_parameter.dict())


  # Edit parameter
  # Param:
  #   @id_param: id of parameter
  #   @data_parameter: data request
  # Return: None
  def edit(self, id_param, data_parameter):
    # Get parameter by id
    param = self.parameters_repo.get_by_id(id_param)
    # Check param exist
    if not param:
      raise CommonException(message=ERR_MESSAGE.MSG_0005)

    # Add parameter
    self.parameters_repo.edit(id_param, data_parameter)


  # Delete parameter
  # Param:
  #   @id_param: id of parameter
  # Return: None
  def delete(self, id_param):
    # Get parameter by id
    param = self.parameters_repo.get_by_id(id_param)
    # Check param exist
    if not param:
      raise CommonException(message=ERR_MESSAGE.MSG_0005)

    # Add parameter
    self.parameters_repo.delete(id_param)
