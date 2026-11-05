from sqlalchemy.orm import Session
from ..models.akademik import Kelas
from ..models.krs import KRSDetail
from ..schemas.akademik import KelasCreate, KelasUpdate


def list(db: Session, tahun_id: int = None, mk_id: int = None,
         dosen_id: int = None, skip: int = 0, limit: int = 200):
    q = db.query(Kelas)
    if tahun_id:
        q = q.filter(Kelas.tahun_akademik_id == tahun_id)
    if mk_id:
        q = q.filter(Kelas.mk_id == mk_id)
    if dosen_id:
        q = q.filter(Kelas.dosen_id == dosen_id)
    return q.order_by(Kelas.kode_kelas).offset(skip).limit(limit).all()


def get(db: Session, kelas_id: int):
    return db.query(Kelas).get(kelas_id)


def get_by_kode(db: Session, mk_id: int, tahun_id: int, kode: str):
    return db.query(Kelas).filter_by(
        mk_id=mk_id, tahun_akademik_id=tahun_id, kode_kelas=kode
    ).first()


def create(db: Session, data: KelasCreate):
    obj = Kelas(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, kelas_id: int, data: KelasUpdate):
    obj = get(db, kelas_id)
    if not obj:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, kelas_id: int):
    if db.query(KRSDetail).filter_by(kelas_id=kelas_id).count() > 0:
        return None
    obj = get(db, kelas_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj


def jumlah_peserta(db: Session, kelas_id: int) -> int:
    return db.query(KRSDetail).filter_by(
        kelas_id=kelas_id, status="aktif"
    ).count()