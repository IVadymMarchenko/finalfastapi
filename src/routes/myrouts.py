from fastapi import APIRouter, HTTPException, Query, Depends, status, Query
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.contacts.models import Contact
from src.db.connectdb import get_db
from src.repository import functiondb
from src.repository import functiondb
from src.schemas.checkschemas import CreateContactSchema, CreateContact

routs = APIRouter(prefix='/contacts', tags=['contacts'])


@routs.get('/', response_model=list[CreateContact])
async def get_contacts(limit: int = Query(10, ge=10, le=100), offset: int = Query(0, ge=0),
                       db: AsyncSession = Depends(get_db)):
    contacts = await functiondb.get_contacts(limit, offset, db)
    return contacts


@routs.get('/{contact_id}', response_model=CreateContactSchema)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await functiondb.get_contact(contact_id, db)
    return contact


@routs.post('/', response_model=CreateContact, status_code=status.HTTP_201_CREATED)
async def create_contact(body: CreateContactSchema, db: AsyncSession = Depends(get_db)):
    contact = await functiondb.create_contact(body, db)
    return contact


@routs.put('/{contact_id}')
async def update_contact(contact_id: int, body: CreateContactSchema, db: AsyncSession = Depends(get_db)):
    contact = await functiondb.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return contact


@routs.delete('/{contact_id}')
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await functiondb.delete_contact(contact_id, db)
    return contact


@routs.get("/birthdays/", response_model=list[CreateContact])
async def get_birthdays(db: AsyncSession = Depends(get_db)):
    return await functiondb.upcoming_birthday(db)




@routs.get('/search_contact/{name_contact_or_surname_or_email}', response_model=CreateContactSchema)
async def look_for_contact(name_contact: str, db: AsyncSession = Depends(get_db)):
    contact = await functiondb.look_for_contact(db, name_contact)
    return contact
