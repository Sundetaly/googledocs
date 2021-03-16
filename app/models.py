from sqlalchemy import Column, Integer, String

from database import Base


class DidPhoneMatch(Base):
    __tablename__ = "did_phone_matches"

    id = Column(Integer, primary_key=True)
    number = Column(String, unique=True)
    name = Column(String)

    def __str__(self):
        return f"{self.number}: {self.name}"