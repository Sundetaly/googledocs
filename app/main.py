from typing import List
from functools import lru_cache
import datetime
import time
from oauth2client.service_account import ServiceAccountCredentials
import gspread

from fastapi import Depends, FastAPI, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


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
    return crud.get_phonematch(db)


@app.post("/phonematch/", response_model=schemas.DidPhoneMatch)
def create_phonematch(phonematch: schemas.DidPhoneMatchCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_phonematch(db, phonematch=phonematch)
    except IntegrityError:
        raise HTTPException(status_code=400, detail='Key (did_number)=(string) already exists.')


@app.post("/report")
async def create_docs(asterisk_item: schemas.AsteriskItem, settings_cash: settings = Depends(get_settings)):
    now = datetime.datetime.strptime(asterisk_item.called_datetime, "%Y-%m-%d %H:%M:%S")
    called_date = datetime.date.strftime(now, "%d.%m.%Y")
    called_time = datetime.date.strftime(now, "%H:%M:%S")
    did = asterisk_item.did
    dst = asterisk_item.dst
    called_num = asterisk_item.called_num
    called_name = asterisk_item.called_name
    wait_time = asterisk_item.wait_time
    talk_time = asterisk_item.talk_time
    wait_time = asterisk_item.wait_time
    disposition = asterisk_item.disposition
    src = asterisk_item.src


    if not talk_time:
        talk_time = 0
    if not wait_time:
        wait_time = 0

    wait_time = int(wait_time)
    talk_time = int(talk_time)

    if talk_time > 0:
        disposition = "ANSWERED"

    called_num = "".join(i for i in called_num if i.isdigit())

    who_hungup = "..."
    if "SIP" in who_hungup:
        who_hungup = "Оператор"
    elif "IAX2" in who_hungup:
        who_hungup = "Клиент"

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        f"{settings_cash.BASE_DIR}/{settings_cash.CREDENTIALS_FILE}",
        ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(credentials)

    if len(src) > 5:  # ????
        wait_time = time.strftime("%M:%S", time.gmtime(wait_time))
        talk_time = time.strftime("%M:%S", time.gmtime(talk_time))
        did = "".join(i for i in did if i.isdigit())

        if called_num[-10:-7] in settings.MOBILE_PHONE_CODES:
            if called_num[1] == 7:
                called_num = '+{}'.format(called_num)

        post_data = [called_date, called_time, did, '', dst, called_num,
                     called_name, wait_time, talk_time, disposition, who_hungup]

        for i in range(len(post_data)):
            if isinstance(post_data[i], bytes):
                post_data[i] = post_data[i].decode("utf-8")

        sheet = client.open(settings.INBOUND_FILE_NAME).sheet1
        sheet.append_row(post_data)

    else:
        wait_time = wait_time - talk_time
        wait_time = time.strftime('%M:%S', time.gmtime(wait_time))
        talk_time = time.strftime('%M:%S', time.gmtime(talk_time))
        if did[-10:-7] in did:
            if did[1] == 7:
                did = '+7{}'.format(did[-10:])
        else:
            did = '+8{}'.format(did[-10:])
        post_data = [called_date, called_time, did, dst,
                     called_num, called_name, wait_time, talk_time,
                     disposition, who_hungup]
        for i in range(len(post_data)):
            if isinstance(post_data[i], bytes):
                post_data[i] = post_data[i].decode("utf-8")

        sheet = client.open(settings.OUTBOUND_FILE_NAME).sheet1
        sheet.append_row(post_data)

    return asterisk_item
