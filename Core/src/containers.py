"""
Definition Containers
"""

from dependency_injector import containers, providers
from crm_member import MemberRepository, MemberService
from crm_shop import ShopRepository, ShopService
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
  member_repository = providers.Factory(MemberRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)

  shop_repository = providers.Factory(ShopRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)

  # service
  shop_service = providers.Factory(ShopService, shop_repository=shop_repository)

  member_service = providers.Factory(MemberService, member_repository=member_repository, shop_repository=shop_repository)