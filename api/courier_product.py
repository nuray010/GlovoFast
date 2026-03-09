from fastapi import APIRouter, HTTPException, Depends
from myproject.database.models import CourierProduct
from myproject.database.schema import CourierProductInputSchema, CourierProductOutSchema
from myproject.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

courier_product_router = APIRouter(prefix='/courier_product', tags=['CourierProduct'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@courier_product_router.post('/', response_model=CourierProductOutSchema)
async def create_courier_product(courier_product: CourierProductInputSchema, db: Session = Depends(get_db)):
    courier_product_db = CourierProduct(**courier_product.dict())
    db.add(courier_product_db)
    db.commit()
    db.refresh(courier_product_db)
    return courier_product_db


@courier_product_router.get('/', response_model=List[CourierProductOutSchema])
async def list_courier_product(db: Session = Depends(get_db)):
    return db.query(CourierProduct).all()


@courier_product_router.get('/{courier_product.id}/', response_model=CourierProductOutSchema)
async def detail_courier_product(courier_product_id: int, db: Session = Depends(get_db)):
    courier_product_db = db.query(CourierProduct).filter(CourierProduct.id == courier_product_id).first()
    if not courier_product_db:
        raise HTTPException(detail='PLease write correctly', status_code=400)

    return courier_product_db


@courier_product_router.put('/{courier_product.id}/', response_model=dict)
async def update_courier_product(courier_product_id: int, courier_product: CourierProductInputSchema,
                                 db: Session = Depends(get_db)):
    courier_product_db = db.query(CourierProduct).filter(CourierProduct.id == courier_product_id).first()
    if not courier_product_db:
        raise HTTPException(detail='PLease write correctly', status_code=400)

    for courier_product_key, courier_product_value in courier_product.dict().items():
        setattr(courier_product_db, courier_product_key, courier_product_value)

        db.commit()
        db.refresh(courier_product_db)
        return {'message': 'Courier product ийгиликтуу озгорулду'}


@courier_product_router.delete('/{courier_product.id}/', response_model=dict)
async def delete_courier_product(courier_product_id: int, db: Session = Depends(get_db)):
    courier_product_db = db.query(CourierProduct).filter(CourierProduct.id == courier_product_id).first()
    if not courier_product_db:
        raise HTTPException(detail='PLease write correctly', status_code=400)

    db.delete(courier_product_db)
    db.commit()
    return {'massage': 'courier product удален'}