"""
Definition Containers
"""

from dependency_injector import containers, providers
from crm_action import ActionRepository, ActionService
from crm_member import MemberRepository, MemberService
from crm_print.repository import PrintRepository
from crm_print.services import PrintService
from crm_shop import ShopRepository, ShopService
from crm_customer import CustomerRepository, CustomerService
from crm_condition_filter import ConditionFilterRepository, ConditionFilterService
from crm_customer_tags import CustomerTagsRepository, CustomerTagsService
from crm_manager_visit_store import ManagerVisitStoreService
from crm_shop_notify import ShopNotifyService, ShopNotifyRepository
from crm_setting_shop import SettingShopService, SettingShopRepository
from crm_service_owner import ServiceOwnerRepository, ServiceOwner
from crm_template import TemplateRepository, TemplateService
from crm_address import AddressRepository, AddressService
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

  condition_filter_repository = providers.Factory(ConditionFilterRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)

  customer_repository = providers.Factory(CustomerRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)

  shop_repository = providers.Factory(ShopRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)

  customer_tags_repository = providers.Factory(CustomerTagsRepository,session_factory=db.provided.session,session_factory_read=db_read.provided.session)

  shop_notify_repository = providers.Factory(ShopNotifyRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)

  setting_shop_repository = providers.Factory(SettingShopRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)

  service_owner_repository = providers.Factory(ServiceOwnerRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)

  template_repository = providers.Factory(TemplateRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)

  action_repository = providers.Factory(ActionRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)

  address_repository = providers.Factory(AddressRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)

  print_repository = providers.Factory(PrintRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)

  # service
  shop_service = providers.Factory(ShopService, shop_repository=shop_repository)

  customer_service = providers.Factory(CustomerService, shop_repository=shop_repository,
                                        customer_repository=customer_repository, condition_filter_repository=condition_filter_repository, action_repository=action_repository)

  condition_filter_service = providers.Factory(ConditionFilterService, condition_filter_repository=condition_filter_repository, customer_repository=customer_repository)

  member_service = providers.Factory(MemberService, member_repository=member_repository, shop_repository=shop_repository)

  customer_tags_service = providers.Factory(CustomerTagsService,
      condition_filter_repository=condition_filter_repository,
      customer_tags_repository=customer_tags_repository,
      customer_repository=customer_repository)

  manager_visit_store_service = providers.Factory(ManagerVisitStoreService, customer_repository=customer_repository, action_repository=action_repository)

  shop_notify_service = providers.Factory(ShopNotifyService, shop_notify_repository=shop_notify_repository)

  setting_shop_service = providers.Factory(SettingShopService, shop_repository=shop_repository,
                                            setting_shop_repository=setting_shop_repository, customer_repository=customer_repository)

  services_owner = providers.Factory(ServiceOwner, service_owner_repository=service_owner_repository)

  template_service = providers.Factory(TemplateService, template_repository=template_repository)

  action_service = providers.Factory(ActionService, action_repository = action_repository,
      service_owner_repository = service_owner_repository, condition_filter_repository = condition_filter_repository,
      customer_tags_repository = customer_tags_repository, customer_repository = customer_repository)

  address_service = providers.Factory(AddressService, address_repository = address_repository)

  print_service = providers.Factory(PrintService, print_repository = print_repository,
      service_owner_repository = service_owner_repository, condition_filter_repository = condition_filter_repository,
      customer_tags_repository = customer_tags_repository, customer_repository = customer_repository)
