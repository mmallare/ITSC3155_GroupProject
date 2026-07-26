from datetime import datetime

from fastapi import HTTPException, Response, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..models import promotions as model


def _database_error_detail(error: SQLAlchemyError) -> str:
    return str(getattr(error, "orig", error))


def create(db: Session, request):
    new_promotion = model.Promotion(
        promo_code=request.promo_code.upper(),
        expiration_date=request.expiration_date,
        discount_percent=request.discount_percent,
        is_active=request.is_active,
    )

    try:
        db.add(new_promotion)
        db.commit()
        db.refresh(new_promotion)
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_database_error_detail(error),
        )

    return new_promotion


def read_all(db: Session):
    try:
        return db.query(model.Promotion).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_database_error_detail(error),
        )


def read_one(db: Session, item_id: int):
    try:
        promotion = db.query(model.Promotion).filter(
            model.Promotion.id == item_id
        ).first()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_database_error_detail(error),
        )

    if not promotion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Promotion id not found!",
        )

    return promotion


def update(db: Session, item_id: int, request):
    promotion = read_one(db, item_id)
    update_data = request.model_dump(exclude_unset=True)

    if "promo_code" in update_data and update_data["promo_code"] is not None:
        update_data["promo_code"] = update_data["promo_code"].upper()

    for field, value in update_data.items():
        setattr(promotion, field, value)

    try:
        db.commit()
        db.refresh(promotion)
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_database_error_detail(error),
        )

    return promotion


def delete(db: Session, item_id: int):
    promotion = read_one(db, item_id)

    try:
        db.delete(promotion)
        db.commit()
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_database_error_detail(error),
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


def validate_code(db: Session, promo_code: str):
    normalized_code = promo_code.strip().upper()

    try:
        promotion = db.query(model.Promotion).filter(
            model.Promotion.promo_code == normalized_code
        ).first()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_database_error_detail(error),
        )

    if not promotion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Promotion code not found!",
        )
    if not promotion.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Promotion is inactive!",
        )
    if promotion.expiration_date <= datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Promotion has expired!",
        )

    return promotion
