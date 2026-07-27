from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..controllers import promotions as controller
from ..dependencies.database import get_db
from ..schemas import promotions as schema


router = APIRouter(
    tags=["Promotions"],
    prefix="/promotions",
)


@router.post("/", response_model=schema.Promotion)
def create(
    request: schema.PromotionCreate,
    db: Session = Depends(get_db),
):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Promotion])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/validate/{promo_code}", response_model=schema.Promotion)
def validate_code(
    promo_code: str,
    db: Session = Depends(get_db),
):
    return controller.validate_code(db=db, promo_code=promo_code)


@router.get("/{item_id}", response_model=schema.Promotion)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Promotion)
def update(
    item_id: int,
    request: schema.PromotionUpdate,
    db: Session = Depends(get_db),
):
    return controller.update(db=db, item_id=item_id, request=request)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
