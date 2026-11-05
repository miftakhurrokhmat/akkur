from sqlalchemy.orm import Session
from ..models.akademik import Dosen, Kelas
from ..schemas.akademik import DosenCreate, DosenUpdate


def list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Dosen).order_by(Dosen.nama).offset(skip).limit(limit).all()


def get(db: Session, dosen_id: int):
    return db.query(Dosen).get(dosen_id)


def get_by_nidn(db: Session, nidn: str):
    return db.query(Dosen).filter_by(nidn=nidn).first()


def create(db: Session, data: DosenCreate):
    obj = Dosen(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, dosen_id: int, data: DosenUpdate):
    obj = get(db, dosen_id)
    if not obj:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, dosen_id: int):
    if db.query(Kelas).filter_by(dosen_id=dosen_id).count() > 0:
        return None
    obj = get(db, dosen_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj