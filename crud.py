from sqlalchemy.orm import Session
import models
import schemas
from sqlalchemy import func
from datetime import datetime, timedelta


def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()


def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update_contact(db: Session, contact_id: int, contact_update: schemas.ContactCreate):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact is None:
        return None

    # Оновлення полів моделі
    for var, value in vars(contact_update).items():
        setattr(db_contact, var, value) if value else None

    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact is None:
        return None

    db.delete(db_contact)
    db.commit()
    return db_contact


def get_contacts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Contact).offset(skip).limit(limit).all()


def search_contacts(db: Session, query: str, skip: int = 0, limit: int = 10):
    return db.query(models.Contact).filter(
        or_(
            models.Contact.first_name.ilike(f"%{query}%"),
            models.Contact.last_name.ilike(f"%{query}%"),
            models.Contact.email.ilike(f"%{query}%")
        )
    ).offset(skip).limit(limit).all()


def get_upcoming_birthdays(db: Session, skip: int = 0, limit: int = 10):
    today = datetime.now().date()
    in_a_week = today + timedelta(days=7)
    return db.query(models.Contact).filter(
        func.date(models.Contact.birthday).between(today, in_a_week)
    ).offset(skip).limit(limit).all()
