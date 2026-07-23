import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import cart as model
from ..schemas import cart as schema
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


def create(db: Session, request: schema.CartCreate):
    new_item = model.Cart(**request.model_dump())

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        logger.info(f"Cart item added: ID={new_item.id}, Table={new_item.table_number}, MenuItem={new_item.menu_item_id}, Qty={new_item.quantity}, Subtotal=${new_item.subtotal}")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        logger.error(f"Failed to add cart item: {error}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.Cart).all()
        logger.debug(f"Retrieved {len(result)} cart items")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        logger.error(f"Failed to retrieve cart items: {error}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Cart).filter(model.Cart.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request: schema.CartUpdate):
    try:
        item = db.query(model.Cart).filter(model.Cart.id == item_id)
        if not item.first():
            logger.warning(f"Update attempted on non-existent cart item ID={item_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.model_dump(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
        logger.info(f"Cart item updated: ID={item_id}, Changes={update_data}")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        logger.error(f"Failed to update cart item ID={item_id}: {error}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Cart).filter(model.Cart.id == item_id)
        if not item.first():
            logger.warning(f"Delete attempted on non-existent cart item ID={item_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
        logger.info(f"Cart item deleted: ID={item_id}")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        logger.error(f"Failed to delete cart item ID={item_id}: {error}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)