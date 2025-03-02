"""
Definition Containers
"""

from dependency_injector import containers, providers
from db.database import Database
from helpers.kbn import TYPE_DB
from user import UserRepository, UserService
from category import CategoryRepository, CategoryService
from kind import KindRepository, KindService
from sale import SaleRepository, SaleService
from image import ImageRepository, ImageService
from product import ProductRepository, ProductService
from setting import SettingRepository, SettingService
from core.logger import get_logger

class Container(containers.DeclarativeContainer):
    """
        Definition Containers   
    """
    logger = providers.Resource(get_logger)

    db = providers.Singleton(Database, db_kbn=TYPE_DB.WRITE)
    db_read = providers.Singleton(Database, db_kbn=TYPE_DB.READ)

    # repository
    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
        session_factory_read=db_read.provided.session
    )
    category_repository = providers.Factory(
        CategoryRepository,
        session_factory=db.provided.session,
        session_factory_read=db_read.provided.session
    )
    kind_repository = providers.Factory(
        KindRepository,
        session_factory=db.provided.session,
        session_factory_read=db_read.provided.session
    )
    sale_repository = providers.Factory(
        SaleRepository,
        session_factory=db.provided.session,
        session_factory_read=db_read.provided.session
    )
    image_repository = providers.Factory(
        ImageRepository,
        session_factory=db.provided.session,
        session_factory_read=db_read.provided.session
    )
    product_repository = providers.Factory(
        ProductRepository,
        session_factory=db.provided.session,
        session_factory_read=db_read.provided.session
    )
    setting_repository = providers.Factory(
        SettingRepository,
        session_factory=db.provided.session,
        session_factory_read=db_read.provided.session
    )

    # service
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )
    category_service = providers.Factory(
        CategoryService,
        category_repository=category_repository,
    )
    kind_service = providers.Factory(
        KindService,
        kind_repository=kind_repository,
    )
    sale_service = providers.Factory(
        SaleService,
        sale_repository=sale_repository,
    )
    image_service = providers.Factory(
        ImageService,
        image_repository=image_repository,
    )
    product_service = providers.Factory(
        ProductService,
        product_repository=product_repository,
        sale_repository=sale_repository,
        image_repository=image_repository,
        category_repository=category_repository
    )
    setting_service = providers.Factory(
        SettingService,
        setting_repository=setting_repository,
    )
