from sqlalchemy.orm import Session

import models, schemas


def get_phonematch(db: Session):
    return db.query(models.DidPhoneMatch).all()


def get_phonematch_by_number(db: Session, number: str):
    return db.query(models.DidPhoneMatch).filter(did_number=number).first()


def create_phonematch(db: Session, phonematch: schemas.DidPhoneMatchCreate):

    db_phonematch = models.DidPhoneMatch(**phonematch.dict())
    db.add(db_phonematch)
    db.commit()
    db.refresh(db_phonematch)

    return db_phonematch
