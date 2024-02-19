from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db=db, contact=contact)


@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact_route(contact_id: int, contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    updated_contact = crud.update_contact(db=db, contact_id=contact_id, contact_update=contact)
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact


@app.delete("/contacts/{contact_id}", response_model=schemas.Contact)
def delete_contact_route(contact_id: int, db: Session = Depends(get_db)):
    deleted_contact = crud.delete_contact(db=db, contact_id=contact_id)
    if deleted_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return deleted_contact


@app.get("/contacts/", response_model=List[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    contacts = crud.get_contacts(db, skip=skip, limit=limit)
    return contacts


@app.get("/contacts/search/", response_model=List[schemas.Contact])
def search_contacts_route(query: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    results = crud.search_contacts(db, query=query, skip=skip, limit=limit)
    return results


@app.get("/contacts/upcoming-birthdays/", response_model=List[schemas.Contact])
def get_upcoming_birthdays_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    results = crud.get_upcoming_birthdays(db, skip=skip, limit=limit)
    return results
