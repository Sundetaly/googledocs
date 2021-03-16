from sqlalchemy.orm import Session

import models, schemas


def get_didphonematch(db: Session):
    return db.query(models.DidPhoneMatch).all()


def create_didphonematch(db: Session, didphonematch: schemas.DidPhoneMatchCreate):
    db_phonematch = models.DidPhoneMatch(**didphonematch.dict())
    db.add(db_phonematch)
    db.commit()
    db.refresh(db_phonematch)

    return db_phonematch
