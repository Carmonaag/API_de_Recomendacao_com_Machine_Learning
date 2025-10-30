from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import repository as db_repository
from app.schemas import item as item_schema
from app.main import get_db

router = APIRouter()

@router.post("/items/", response_model=item_schema.Item)
def create_item(item: item_schema.ItemCreate, db: Session = Depends(get_db)):
    return db_repository.create_item(db=db, item=item)

@router.get("/items/", response_model=list[item_schema.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db_repository.get_items(db, skip=skip, limit=limit)
    return items
