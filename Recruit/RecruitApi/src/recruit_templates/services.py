"""
Templates Service
"""
from core import CommonException, ERR_MESSAGE
from recruit_templates import TemplatesRepository


class TemplatesService:
  """
    Templates service
  """
  def __init__(self, templates_repository: TemplatesRepository):
    self.templates_repo: TemplatesRepository = templates_repository


  # Get list templates
  # Param: None
  # Return: list item template
  def get_list(self):
    list_templates = self.templates_repo.get_list()
    # Check template exist
    if not list_templates:
      raise CommonException(message=ERR_MESSAGE.MSG_0005)

    return list_templates


  # Get template by id template
  # Param:
  #   @id_template: id of template
  # Return: list item template
  def get_by_id(self, id_template):
    template = self.templates_repo.get_by_id(id_template)
    # Check template exist
    if not template:
      raise CommonException(message=ERR_MESSAGE.MSG_0005)

    return template


  # Edit template mail
  # Param:
  #   @id_template: id of template
  #   @data_template: data request
  # Return: None
  def edit(self, id_template, data_template):
    template = self.templates_repo.get_by_id(id_template)
    # Check template exist
    if not template:
      raise CommonException(message=ERR_MESSAGE.MSG_0005)

    # Update mail template
    self.templates_repo.edit(id_template, data_template.dict())
