from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.connectdb import get_db
from src.contacts.models import User
from src.schemas.user import UserSchema
from src.contacts.models import User


async def create_user(body: UserSchema, db: AsyncSession):
    new_user = User(**body.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    smt = select(User).filter_by(email=email)
    user = await db.execute(smt)
    user = user.scalar_one_or_none()
    return user


async def update_token(user: User, token: str | None, db: AsyncSession):
    user.refresh_token = token
    await db.commit()
