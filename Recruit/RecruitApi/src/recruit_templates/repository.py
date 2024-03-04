"""
Repository template
"""

from core import CommonRepository
from models import Templates
from helpers import kbn
from fastapi.encoders import jsonable_encoder
import re

class TemplatesRepository(CommonRepository):
  """
  Repository of template
  """

  # Get list templates
  # Params: None
  # Output: list template
  def get_list(self):
    with self.session_factory_read() as session:
      query = session.query(Templates).filter(Templates.is_deleted == kbn.DeleteFlag.OFF.value)
      count_param = query.count()

      return {
        "list_templates": jsonable_encoder(query.all()),
        "count": count_param,
      }


  # Get template by id template
  # Params:
  #   @id_template: id of template
  # Output: item template
  def get_by_id(self, id_template):
    with self.session_factory_read() as session:
      return jsonable_encoder(session.query(Templates).filter(Templates.id == id_template, Templates.is_deleted == kbn.DeleteFlag.OFF.value).first())


  # Update mail template
  # Params:
  #   @id_template: id of template
  #   @data_template: data request of template
  # Output: None
  def edit(self, id_template, data_template):
    with self.session_factory_read() as session:
      session.query(Templates).filter(
        Templates.id == id_template, Templates.is_deleted == kbn.DeleteFlag.OFF.value
      ).update({
        Templates.title: data_template["title"],
        Templates.body: data_template["body"],
        Templates.note: data_template["note"],
      })
      session.commit()


  # Get template by key
  # Params:
  #   @key_template: key template
  # Output: Template
  def get_template_by_key(self, key_template: str):
    with self.session_factory_read() as session:
      params = []
      template = jsonable_encoder(session.query(Templates).filter(
        Templates.key == key_template,
        Templates.is_deleted == kbn.DeleteFlag.OFF.value
      ).first())

      params.extend(re.findall("\\$[A-Za-z\_]+", template["title"]))
      params.extend(re.findall("\\$[A-Za-z\_]+", template["body"]))
      for index, param in enumerate(params):
        params[index] = param.replace("$", "")
      template["params"] = list(set(params))

      return template
