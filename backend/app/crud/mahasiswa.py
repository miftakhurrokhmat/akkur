from sqlalchemy.orm import Session
from ..models.akademik import Mahasiswa
from ..models.krs import KRS
from ..schemas.akademik import MahasiswaCreate, MahasiswaUpdate


def list(db: Session, skip: int = 0, limit: int = 100,
         angkatan: int = None, prodi: str = None, status: str = None):
    q = db.query(Mahasiswa)
    if angkatan:
        q = q.filter(Mahasiswa.angkatan == angkatan)
    if prodi:
        q = q.filter(Mahasiswa.prodi == prodi)
    if status:
        q = q.filter(Mahasiswa.status == status)
    return q.order_by(Mahasiswa.nim).offset(skip).limit(limit).all()


def get(db: Session, mhs_id: int):
    return db.query(Mahasiswa).get(mhs_id)


def get_by_nim(db: Session, nim: str):
    return db.query(Mahasiswa).filter_by(nim=nim).first()


def create(db: Session, data: MahasiswaCreate):
    obj = Mahasiswa(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, mhs_id: int, data: MahasiswaUpdate):
    obj = get(db, mhs_id)
    if not obj:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, mhs_id: int):
    if db.query(KRS).filter_by(mahasiswa_id=mhs_id).count() > 0:
        return None
    obj = get(db, mhs_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj