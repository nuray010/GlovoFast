from fastapi import APIRouter, HTTPException, Depends
from myproject.database.models import UserProfile
from myproject.database.schema import UserprofileInputSchema,UserprofileOutSchema
from myproject.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

user_router = APIRouter(prefix='/users',tags=['Users'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@user_router.post("/",response_model=UserprofileOutSchema)
async def create_user(user: UserprofileInputSchema, db: Session = Depends(get_db)):
  user_db = UserProfile(**user.dict())
  db.add(user_db)
  db.commit()
  db.refresh(user_db)
  return user_db


@user_router.get('/',response_model=List[UserprofileOutSchema])
async def list_user(db: Session = Depends(get_db)):
     return db.query(UserProfile).all()

@user_router.get('/{user.id}/',response_model=UserprofileOutSchema)
async def detail_user(user_id: int,db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if not user_db:
        raise HTTPException(detail='PLease write correctly',status_code=400)

    return user_db

@user_router.put('/{user.id}/',response_model=dict)
async def update_user(user_id: int, user: UserprofileInputSchema ,
                          db: Session = Depends(get_db)):
    user_db =  db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if not user_db:
        raise HTTPException(detail='PLease write correctly', status_code=400)

    for user_key,user_value in user.dict().items():
        setattr(user_db,user_key,user_value)

        db.commit()
        db.refresh(user_db)
        return {'message': 'user озгорулду'}


@user_router.delete('/{user.id}/',response_model=dict)
async def delete_user(user_id: int,db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(detail='PLease write correctly', status_code=400)

    db.delete(user_db)
    db.commit()
    return {'massage': 'user удален'}