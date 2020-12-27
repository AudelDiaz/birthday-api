from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/v1/friends/", response_model=List[schemas.Friend])
def list_friends(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_friends(db, skip=skip, limit=limit)
    return items


@app.get("/api/v1/friends/{friend_id}", response_model=schemas.Friend)
def get_friend_by_id(friend_id: int, db: Session = Depends(get_db)):
    result = crud.get_user(db, friend_id=friend_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Friend not found")
    return result


@app.post("/api/v1/friends/", response_model=schemas.Friend)
def create_friend(friend: schemas.FriendCreate, db: Session = Depends(get_db)):
    db_user = crud.get_friend_by_email(db, email=friend.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_friend(db=db, friend=friend)


@app.get("/api/v1/friends/birthdays/month/{month}", response_model=List[schemas.Friend])
def get_birthdays_by_month(month: int, db: Session = Depends(get_db)):
    if 1 <= month <= 12:
        return crud.get_birthdays(db=db, month=month)
    else:
        raise HTTPException(status_code=400, detail="The month param should be a number between 1 and 12.")


@app.get("/api/v1/friends/birthdays/month/{month}/day/{day}", response_model=List[schemas.Friend])
def get_birthday_by_day(month: int, day: int, db: Session = Depends(get_db)):
    if 1 <= month <= 12 and 1 <= day <= 31:
        return crud.get_birthdays(db=db, month=month, day=day)
    elif 1 <= month <= 12:
        raise HTTPException(status_code=400, detail="The day param should be a number between 1 and 31.")
    else:
        raise HTTPException(status_code=400, detail="The month param should be a number between 1 and 12.")


@app.get("/api/v1/friends/birthdays/today/", response_model=List[schemas.Friend])
def get_today_birthdays(db: Session = Depends(get_db)):
    return crud.get_today_birthdays(db=db)
