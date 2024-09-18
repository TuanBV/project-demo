"""
Definition Containers
"""

from dependency_injector import containers, providers
from db.database import Database
from helpers.kbn import TYPE_DB
from users import UsersRepository, UsersService
from core.logger import get_logger

class Container(containers.DeclarativeContainer):
  """
  Class Containers
  """
  wiring_config = containers.WiringConfiguration(modules=["routers"])
  config = providers.Configuration()

  logger = providers.Resource(get_logger)

  db = providers.Singleton(Database, db_kbn=TYPE_DB.WRITE)
  db_read = providers.Singleton(Database, db_kbn=TYPE_DB.READ)

  # repository
  users_repository = providers.Factory(UsersRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)


  # service
  users_service = providers.Factory(
    UsersService,
    users_repository=users_repository
  )
