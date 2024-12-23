"""
Definition Containers
"""

from dependency_injector import containers, providers
from db.database import Database
from helpers.kbn import TYPE_DB
from user import UserRepository, UserService
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

    # service
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )
