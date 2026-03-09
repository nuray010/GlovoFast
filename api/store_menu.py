from fastapi import APIRouter, HTTPException, Depends
from myproject.database.models import StoreMenu
from myproject.database.schema import StoreMenuInputSchema, StoreMenuOutSchema
from myproject.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

store_menu_router = APIRouter(prefix='/store_menu', tags=['StoreMenu'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@store_menu_router.post('/', response_model=StoreMenuOutSchema)
async def create_store_menu(store_menu: StoreMenuInputSchema, db: Session = Depends(get_db)):
    store_menu_db = StoreMenu(**store_menu.dict())
    db.add(store_menu_db)
    db.commit()
    db.refresh(store_menu_db)
    return store_menu_db


@store_menu_router.get('/', response_model=List[StoreMenuOutSchema])
async def list_store_menu(db: Session = Depends(get_db)):
    return db.query(StoreMenu).all()


@store_menu_router.get('/{store_menu.id}/', response_model=StoreMenuOutSchema)
async def detail_store_menu(store_menu_id: int, db: Session = Depends(get_db)):
    store_menu_db = db.query(StoreMenu).filter(StoreMenu.id == store_menu_id).first()
    if not store_menu_db:
        raise HTTPException(detail='PLease write correctly', status_code=400)

    return store_menu_db


@store_menu_router.put('/{store_menu.id}/', response_model=dict)
async def update_store_menu(store_menu_id: int, store_menu: StoreMenuInputSchema,
                            db: Session = Depends(get_db)):
    store_menu_db = db.query(StoreMenu).filter(StoreMenu.id == store_menu_id).first()
    if not store_menu_db:
        raise HTTPException(detail='PLease write correctly', status_code=400)

    for store_menu_key, store_menu_value in store_menu.dict().items():
        setattr(store_menu_db, store_menu_key, store_menu_value)

        db.commit()
        db.refresh(store_menu_db)
        return {'message': 'StoreMenu ийгиликтуу озгорулду'}


@store_menu_router.delete('/{store_menu.id}/', response_model=dict)
async def delete_store_menu(store_menu_id: int, db: Session = Depends(get_db)):
    store_menu_db = db.query(StoreMenu).filter(StoreMenu.id == store_menu_id).first()
    if not store_menu_db:
        raise HTTPException(detail='PLease write correctly', status_code=400)

    db.delete(store_menu_db)
    db.commit()
    return {'massage': 'store menu удален'}