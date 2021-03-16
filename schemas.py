from typing import Optional

from pydantic import BaseModel


class AsteriskItem(BaseModel):
    called_datetime: str
    did: str
    dst: str
    called_num: str
    wait_time: Optional[str] = None
    talk_time: Optional[str] = None
    disposition: str
    who_hungup: str
    src: str


class DidPhoneMatchBase(BaseModel):
    did_number: str
    did_name: str


class DidPhoneMatchCreate(DidPhoneMatchBase):
    pass


class DidPhoneMatch(DidPhoneMatchBase):
    id: int

    class Config:
        orm_mode = True
