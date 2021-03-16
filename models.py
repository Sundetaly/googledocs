from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class DidPhoneMatch(Base):
    __tablename__ = 'did_phone_matches'

    id = Column(Integer, primary_key=True)
    did_number = Column(String, unique=True)
    did_name = Column(String)

    def __str__(self):
        return f'{self.did_number}: {self.did_name}'