from pydantic import BaseModel


class DidPhoneMatchBase(BaseModel):
    did_number: str
    did_name: str


class DidPhoneMatchCreate(DidPhoneMatchBase):
    pass


class DidPhoneMatch(DidPhoneMatchBase):
    id: int

    class Config:
        orm_mode = True