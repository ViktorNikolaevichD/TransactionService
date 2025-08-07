from apps.accounting.models import Account, Transaction
from settings.repositories import SQLAlchemyORMRepository


class AccountRepository(SQLAlchemyORMRepository[Account]):
    cls_model = Account


class TransactionRepository(SQLAlchemyORMRepository[Transaction]):
    cls_model = Transaction
