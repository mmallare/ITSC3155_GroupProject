from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import cart as controller
from ..schemas import cart as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Carts'],
    prefix="/carts"
)


@router.post("/", response_model=schema.Cart)
def create(request: schema.CartCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Cart])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{cart_id}", response_model=schema.Cart)
def read_one(cart_id: int, db: Session = Depends(get_db)):
    return controller.read_one_cart(db, cart_id=cart_id)


@router.put("/{cart_id}", response_model=schema.Cart)
def update(cart_id: int, request: schema.CartUpdate, db: Session = Depends(get_db)):
    return controller.update_cart(db=db, request=request, cart_id=cart_id)


@router.delete("/{cart_id}")
def delete(cart_id: int, db: Session = Depends(get_db)):
    return controller.delete_cart(db=db, cart_id=cart_id)