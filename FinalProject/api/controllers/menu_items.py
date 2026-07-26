from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import menu_items as model
from sqlalchemy.exc import SQLAlchemyError
from ..schemas import menu_items as schemas



def create(db: Session, request: schemas.MenuItemCreate):
    db_menu_item = model.MenuItem(
        item_name=request.item_name,
        item_price=request.item_price,
        calories=request.calories
    )

    try:
        db.add(db_menu_item)
        db.commit()
        db.refresh(db_menu_item)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return db_menu_item

def read_all_menu_items(db: Session):
    try:
        result = db.query(model.MenuItem).all()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return result

def read_one_menu_item(db: Session, item_id: int):
    try:
        item = db.query(model.MenuItem).filter(model.MenuItem.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu Item not found.")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return item

def update_menu_item(db: Session, item_id: int, request: schemas.MenuItemUpdate):
    try:
        existing_item = db.query(model.MenuItem).filter(model.MenuItem.id == item_id).first()

        if existing_item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu Item not found.")

        update_data = request.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(existing_item, field, value)

        db.commit()
        db.refresh(existing_item)
        return existing_item

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

def delete_menu_item(db: Session, item_id: int):
    try:
        existing_item = db.query(model.MenuItem).filter(model.MenuItem.id == item_id).first()

        if existing_item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu Item not found.")

        db.delete(existing_item)
        db.commit()
        return existing_item

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))