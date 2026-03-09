from fastapi import APIRouter, HTTPException, Depends
from myproject.database.models import Address
from myproject.database.schema import AddressInputSchema, AddressOutSchema
from myproject.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

address_router = APIRouter(prefix='/address', tags=['Address'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@address_router.post('/', response_model=AddressOutSchema)
async def create_address(address: AddressInputSchema, db: Session = Depends(get_db)):
    address_db = Address(**address.dict())
    db.add(address_db)
    db.commit()
    db.refresh(address_db)
    return address_db


@address_router.get('/', response_model=List[AddressOutSchema])
async def list_address(db: Session = Depends(get_db)):
    return db.query(Address).all()


@address_router.get('/{address.id}/', response_model=AddressOutSchema)
async def detail_address(address_id: int, db: Session = Depends(get_db)):
    address_db = db.query(Address).filter(Address.id == address_id).first()
    if not address_db:
        raise HTTPException(detail='PLease write correctly', status_code=400)

    return address_db


@address_router.put('/{address.id}/', response_model=dict)
async def update_address(address_id: int, address: AddressInputSchema,
                         db: Session = Depends(get_db)):
    address_db = db.query(Address).filter(Address.id == address_id).first()
    if not address_db:
        raise HTTPException(detail='PLease write correctly', status_code=400)

    for address_key, address_value in address.dict().items():
        setattr(address_db, address_key, address_value)

        db.commit()
        db.refresh(address_db)
        return {'message': 'Address ийгиликтуу озгорулду'}


@address_router.delete('/{address.id}/', response_model=dict)
async def delete_address(address_id: int, db: Session = Depends(get_db)):
    address_db = db.query(Address).filter(Address.id == address_id).first()
    if not address_db:
        raise HTTPException(detail='PLease write correctly', status_code=400)

    db.delete(address_db)
    db.commit()
    return {'massage': 'address удален'}