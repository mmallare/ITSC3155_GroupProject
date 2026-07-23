from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..controllers import statistics as controller
from ..dependencies.database import get_db
from ..schemas import statistics as schema


router = APIRouter(
    tags=["Statistics"],
    prefix="/statistics"
)


@router.post("/", response_model=schema.Statistic)
def create(
    request: schema.StatisticCreate,
    db: Session = Depends(get_db)
):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Statistic])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db=db)


@router.get("/{item_id}", response_model=schema.Statistic)
def read_one(
    item_id: int,
    db: Session = Depends(get_db)
):
    return controller.read_one(db=db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Statistic)
def update(
    item_id: int,
    request: schema.StatisticUpdate,
    db: Session = Depends(get_db)
):
    return controller.update(
        db=db,
        item_id=item_id,
        request=request
    )


@router.delete("/{item_id}", status_code=204)
def delete(
    item_id: int,
    db: Session = Depends(get_db)
):
    return controller.delete(db=db, item_id=item_id)