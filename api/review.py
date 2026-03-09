from fastapi import APIRouter, HTTPException, Depends
from myproject.database.models import Review
from myproject.database.schema import ReviewInputShema,ReviewOutShema
from myproject.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

review_router = APIRouter(prefix='/review',tags=['Review'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@review_router.post('/',response_model=ReviewOutShema)
async def create_review(review:ReviewInputShema,db: Session = Depends(get_db)):
    review_db = Review(**review.dict())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db


@review_router.get('/',response_model=List[ReviewOutShema])
async def list_review(db: Session = Depends(get_db)):
     return db.query(Review).all()

@review_router.get('/{review.id}/',response_model=ReviewOutShema)
async def detail_review(review_id: int,db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id==review_id).first()
    if not review_db:
        raise HTTPException(detail='PLease write correctly',status_code=400)

    return review_db


@review_router.put('/{review.id}/',response_model=dict)
async def update_review(review_id: int, review: ReviewInputShema ,
                          db: Session = Depends(get_db)):
    review_db =  db.query(Review).filter(Review.id==review_id).first()
    if not review_db:
        raise HTTPException(detail='PLease write correctly', status_code=400)

    for review_key,review_value in review.dict().items():
        setattr(review_db,review_key,review_value)

        db.commit()
        db.refresh(review_db)
        return {'message': 'review озгорулду'}


@review_router.delete('/{review.id}/',response_model=dict)
async def delete_review(review_id: int,db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(detail='PLease write correctly', status_code=400)

    db.delete(review_db)
    db.commit()
    return {'massage': 'review is deleted'}