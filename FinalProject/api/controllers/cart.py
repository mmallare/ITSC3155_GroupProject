from httpx import request
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import cart as model
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request):
    db_cart = model.Cart(
        subtotal=request.subtotal,
        coupon=request.coupon,
        quantity=request.quantity,
        customer_id=request.customer_id,
        menu_item_id=request.menu_item_id
    )

    try:
        db.add(db_cart)
        db.commit()
        db.refresh(db_cart)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return db_cart


def read_all(db: Session):
    try:
        result = db.query(model.Cart).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def read_one_cart(db: Session, cart_id):
    try:
        cart = db.query(model.Cart).filter(model.Cart.id == cart_id).first()
        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return cart

def update_cart(db: Session, cart_id, request):
    try:
        cart = db.query(model.Cart).filter(model.Cart.id == cart_id)
        existing_cart = cart.first()

        if not existing_cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found")

        update_data = request.dict(exclude_unset=True)
        cart.update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(existing_cart)
        return existing_cart

    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def delete_cart(db: Session, cart_id):
    try:
        cart = db.query(model.Cart).filter(model.Cart.id == cart_id)

            # Used to check if a cart object really exist
        existing_cart = cart.first()
        if not existing_cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found")

        cart.delete(synchronize_session=False)
        db.commit()
        return existing_cart

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


