from apps.user.models import User
from settings.repositories import SQLAlchemyORMRepository


class UserRepository(SQLAlchemyORMRepository[User]):
    cls_model = User
