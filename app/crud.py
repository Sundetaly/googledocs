from sqlalchemy.orm import Session

import models, schemas


def get_phonematch(db: Session):
    return db.query(models.DidPhoneMatch).all()


def create_phonematch(db: Session, phonematch: schemas.DidPhoneMatchCreate):

    db_phonematch = models.DidPhoneMatch(**phonematch.dict())
    db.add(db_phonematch)
    db.commit()
    db.refresh(db_phonematch)

    return db_phonematch
