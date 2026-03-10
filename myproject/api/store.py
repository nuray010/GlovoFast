from fastapi import APIRouter, HTTPException, Depends
from myproject.database.models import Store
from myproject.database.schema import StoreInputSchema, StoreOutSchema
from myproject.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

store_router = APIRouter(prefix='/store', tags=['Store'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@store_router.post('/', response_model=StoreOutSchema)
async def create_store(store: StoreInputSchema, db: Session = Depends(get_db)):
    store_db = Store(**store.dict())
    db.add(store_db)
    db.commit()
    db.refresh(store_db)
    return store_db


@store_router.get('/', response_model=List[StoreOutSchema])
async def list_store(db: Session = Depends(get_db)):
    return db.query(Store).all()


@store_router.get('/{store.id}/', response_model=StoreOutSchema)
async def detail_store(store_id: int, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if not store_db:
        raise HTTPException(detail='PLease write correctly', status_code=400)

    return store_db


@store_router.put('/{store.id}/', response_model=dict)
async def update_store(store_id: int, store: StoreInputSchema,
                       db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if not store_db:
        raise HTTPException(detail='PLease write correctly', status_code=400)

    for store_key, store_value in store.dict().items():
        setattr(store_db, store_key, store_value)

        db.commit()
        db.refresh(store_db)
        return {'message': 'Store ийгиликтуу озгорулду'}


@store_router.delete('/{store.id}/', response_model=dict)
async def delete_store(store_id: int, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if not store_db:
        raise HTTPException(detail='PLease write correctly', status_code=400)

    db.delete(store_db)
    db.commit()
    return {'massage': 'store удален'}