from typing import List
import datetime
import time
from oauth2client.service_account import ServiceAccountCredentials
import gspread

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from functools import lru_cache

from config import settings
from database import engine, SessionLocal
import crud, models, schemas


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@lru_cache()
def get_settings():
    return settings

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/phonematch/", response_model=List[schemas.DidPhoneMatch])
def read_phonematch(db: Session = Depends(get_db)):
    return crud.get_didphonematch(db)


@app.post("/phonematch/", response_model=schemas.DidPhoneMatch)
def create_phonematch(phonematch: schemas.DidPhoneMatchCreate, db: Session = Depends(get_db)):
    return crud.create_didphonematch(db, didphonematch=phonematch)


@app.post("/report")
async def create_docs(asterisk_item: schemas.AsteriskItem, settings_cash: settings = Depends(get_settings)):
    print(settings_cash.CREDENTIALS_FILE)
    now = datetime.datetime(asterisk_item.called_datetime, "%Y-%m-%d %H:%M:%S")
    called_date = datetime.date.strftime(now, "%d.%m.%Y")
    called_time = datetime.date.strftime(now, "%H:%M:%S")
    did = asterisk_item.did
    called_num = asterisk_item.called_num
    wait_time = asterisk_item.wait_time
    talk_time = asterisk_item.talk_time
    wait_time = asterisk_item.wait_time
    disposition = asterisk_item.disposition
    src = asterisk_item.src
    dst = asterisk_item.dst

    if not talk_time:
        talk_time = 0
    wait_time = int(wait_time)
    talk_time = int(talk_time)
    called_num = "".join(i for i in called_num if i.isdigit())
    who_hungup = "..."
    if "SIP" in who_hungup:
        who_hungup = "Оператор"
    elif "IAX2" in who_hungup:
        who_hungup = "Клиент"

    if talk_time > 0:
        disposition = "ANSWERED"

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        f"{settings_cash.BASE_DIR}/{settings_cash.CREDENTIALS_FILE}",
        ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(credentials)
    if len(src) > 5:  # ????
        wait_time = time.strftime("%M:%S", time.gmtime(wait_time))
        talk_time = time.strftime("%M:%S", time.gmtime(talk_time))
        did = "".join(i for i in did if i.isdigit())
    return asterisk_item
