from typing import Any

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.accounting.models import Account, Transaction
from settings.repositories import SQLAlchemyORMRepository
from utils import with_session


class AccountRepository(SQLAlchemyORMRepository[Account]):
    cls_model = Account


class TransactionRepository(SQLAlchemyORMRepository[Transaction]):
    cls_model = Transaction

    @with_session
    async def create_transaction(self, session: AsyncSession, data: dict[str, Any]) -> Transaction:
        async with session.begin():
            stmt = select(Transaction).filter_by(id=data["transaction_id"]).limit(1)
            result = await session.execute(stmt)
            transaction = result.scalar_one_or_none()

            if transaction:
                return transaction
            
            stmt = select(Account).filter_by(id=data["account_id"]).limit(1)
            result = await session.execute(stmt)
            account = result.scalar_one_or_none()

            if not account:
                stmt = insert(Account).values(id=data["account_id"], user_id=data["user_id"], balance=0)
                result = await session.execute(stmt)
            
            stmt = update(Account).filter_by(id=data["account_id"]).values(balance=Account.balance + data["amount"])
            result = await session.execute(stmt)
        
            stmt = insert(Transaction).values(
                id=data["transaction_id"], 
                account_id=data["account_id"], 
                amount=data["amount"],
            ).returning(Transaction)
            result = await session.execute(stmt)
            transaction = result.scalar_one()
            return transaction
