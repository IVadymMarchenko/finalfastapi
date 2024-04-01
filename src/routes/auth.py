from fastapi import APIRouter, HTTPException, Query, Depends, status, Query

from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository import functionuser
from src.db.connectdb import get_db
from src.schemas.user import UserSchema, UserResponse, TokenUpdate
from src.services.auth import auth_service
from src.contacts.models import User
routs = APIRouter(prefix='/auth', tags=['auth'])
get_refresh_token = HTTPBearer()


@routs.post('/signup', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserSchema, db: AsyncSession = Depends(get_db)):
    exist_user = await functionuser.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Account already exist')
    body.password = auth_service.get_password_hash(body.password)
    new_user = await functionuser.create_user(body, db)
    return new_user


@routs.post('/login', response_model=TokenUpdate)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await functionuser.get_user_by_email(body.username, db)
    print('one')
    if user is None:
        print('two')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid email')
    if not auth_service.verify_password(body.password, user.password):
        print('tree')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid password')
    access_token = await auth_service.create_access_token(data={'sub': user.email})
    refresh_token = await auth_service.create_refresh_token(data={'sub': user.email})
    await functionuser.update_token(user, refresh_token, db)
    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}
