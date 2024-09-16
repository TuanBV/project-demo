"""
Definition Containers
"""

from dependency_injector import containers, providers
from user import UserRepository, UserService
from db.database import Database
from helpers.kbn import TYPE_DB


class Container(containers.DeclarativeContainer):
  """
  Class Containers
  """
  wiring_config = containers.WiringConfiguration(modules=["routers"])
  config = providers.Configuration()

  db = providers.Singleton(Database, db_kbn=TYPE_DB.WRITE)
  db_read = providers.Singleton(Database, db_kbn=TYPE_DB.READ)


  # repository
  user_repository = providers.Factory(UserRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)

  # service
  user_service = providers.Factory(UserService, shop_repository=user_repository)