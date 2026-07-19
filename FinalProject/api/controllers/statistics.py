from fastapi import HTTPException, Response, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..models import statistics as model


def create(db: Session, request):
    new_statistic = model.Statistic(
        menu_item_id=request.menu_item_id,
        menu_order_count=request.menu_order_count,
        rating_score=request.rating_score,
        avg_money_spent=request.avg_money_spent,
        peak_hours_traffic=request.peak_hours_traffic,
        frequency=request.frequency
    )

    try:
        db.add(new_statistic)
        db.commit()
        db.refresh(new_statistic)
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(getattr(error, "orig", error))
        )

    return new_statistic


def read_all(db: Session):
    try:
        return db.query(model.Statistic).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(getattr(error, "orig", error))
        )


def read_one(db: Session, item_id: int):
    try:
        statistic = (
            db.query(model.Statistic)
            .filter(model.Statistic.id == item_id)
            .first()
        )

        if statistic is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Statistic ID not found!"
            )

        return statistic
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(getattr(error, "orig", error))
        )


def update(db: Session, item_id: int, request):
    try:
        statistic = (
            db.query(model.Statistic)
            .filter(model.Statistic.id == item_id)
            .first()
        )

        if statistic is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Statistic ID not found!"
            )

        if hasattr(request, "model_dump"):
            update_data = request.model_dump(exclude_unset=True)
        else:
            update_data = request.dict(exclude_unset=True)

        for field, value in update_data.items():
            setattr(statistic, field, value)

        db.commit()
        db.refresh(statistic)
        return statistic

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(getattr(error, "orig", error))
        )


def delete(db: Session, item_id: int):
    try:
        statistic = (
            db.query(model.Statistic)
            .filter(model.Statistic.id == item_id)
            .first()
        )

        if statistic is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Statistic ID not found!"
            )

        db.delete(statistic)
        db.commit()

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(getattr(error, "orig", error))
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)