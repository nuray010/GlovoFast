from fastapi import APIRouter,HTTPException,Depends
from myproject.database.db import SessionLocal
from myproject.database.models import UserProfile,RefreshToken
from myproject.database.schema import UserprofileInputSchema,UserprofileOutSchema,UserLoginShema
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta,datetime
from config import ACCESS_TOKEN_LIFETIME,REFRESH_TOKEN_LIFETIME,SECRET_KEY
from jose import jwt
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_shema = OAuth2PasswordBearer(tokenUrl="/auth/login")


auth_router = APIRouter(prefix='/auth',tags=['Auth'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta]= None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_LIFETIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    return create_access_token(data,expires_delta=timedelta(days=REFRESH_TOKEN_LIFETIME))

@auth_router.post('/register/',response_model=dict)
async def register(user:UserprofileInputSchema,db: Session = Depends(get_db)):
   user_db =  db.query(UserProfile).filter(UserProfile.user_name==user.user_name).first()
   email_db = db.query(UserProfile).filter(UserProfile.email == user.email).first()
   if user_db or email_db:
       raise HTTPException(detail='Мындай username же почта бар экен ',status_code=400)

   hash_password = get_password_hash(user.password)
   user_data = UserProfile(
       first_name = user.first_name,
       last_name = user.last_name,
       user_name = user.user_name,
       email = user.email,
       age = user.age,
       phone_number = user.phone_number,
       password = hash_password
   )


   db.add(user_data)
   db.commit()
   db.refresh(user_data)
   return {'message': 'Сиз регистрация Болдунуз'}


@auth_router.post('/login/',response_model=dict)
async def login(user:UserLoginShema,db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.user_name==user.user_name).first()
    if  not user_db or not verify_password(user.password,user_db.password):
        raise HTTPException(detail='Сиз жазган маалымат туура эмес',status_code=401)


    access_token = create_access_token({'sub': user_db.user_name})
    refresh_token = create_refresh_token({'sub': user_db.user_name})

    token_db = RefreshToken(user_id=user_db.id,token=refresh_token)
    db.add(token_db)
    db.commit()

    return {'access_token': access_token,'refresh_token':refresh_token,'token_type':'Bearer'}


@auth_router.post('/logout')
async def logout(refresh_token:str, db:Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not stored_token:
        raise HTTPException(status_code=401,detail='Маалымат туура эмес')

    db.delete(stored_token)
    db.commit()

    return {"message": 'Вышли'}



@auth_router.post('/refresh')
async def refresh(refresh_token: str,db:Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored_token:
        raise HTTPException(status_code=401,detail='Маалымат туура эмес')

    access_token = create_access_token({'sub': stored_token.id})

    return {'access_token': access_token,'token_type':'Bearer'}

