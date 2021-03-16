from typing import Optional

from pydantic import BaseModel


class AsteriskItem(BaseModel):
    called_datetime: str
    did: str
    dst: str
    called_num: str
    called_name: str
    wait_time: Optional[str] = None
    talk_time: Optional[str] = None
    disposition: str
    who_hungup: str
    src: str
