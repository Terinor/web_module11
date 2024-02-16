from pydantic import BaseModel, EmailStr
from datetime import date


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date


class ContactCreate(ContactBase):
    pass


class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True
