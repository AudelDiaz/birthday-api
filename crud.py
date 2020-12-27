from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import extract
import models
import schemas


def get_friends(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Friend).offset(skip).limit(limit).all()


def get_friend_by_email(db: Session, email: str):
    return db.query(models.Friend).filter(models.Friend.email == email).first()


def get_user(db: Session, friend_id: int):
    return db.query(models.Friend).filter(models.Friend.id == friend_id).first()


def create_friend(db: Session, friend: schemas.FriendCreate):
    db_friend = models.Friend(email=friend.email, first_name=friend.first_name, last_name=friend.last_name,
                              birthdate=friend.birthdate)
    db.add(db_friend)
    db.commit()
    db.refresh(db_friend)
    return db_friend


def get_birthdays(db: Session, month: int, day: int = 0):
    if day == 0:
        return db.query(models.Friend).filter(extract('month', models.Friend.birthdate) == month).all()
    else:
        return db.query(models.Friend).filter(extract('month', models.Friend.birthdate) == month,
                                              extract('day', models.Friend.birthdate) == day).all()


def get_today_birthdays(db: Session):
    today = datetime.today()
    month = extract('month', today)
    day = extract('day', today)
    return get_birthdays(db=db, month=month, day=day)
