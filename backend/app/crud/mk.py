from sqlalchemy.orm import Session
from ..models.kurikulum import MK, CPMK
from ..models.akademik import Kelas
from ..schemas.kurikulum import MKCreate, MKUpdate


def list(db: Session, semester: int = None, skip: int = 0, limit: int = 100):
    q = db.query(MK)
    if semester:
        q = q.filter(MK.semester == semester)
    return q.order_by(MK.semester, MK.kode).offset(skip).limit(limit).all()


def get(db: Session, mk_id: int):
    return db.query(MK).get(mk_id)


def get_by_kode(db: Session, kode: str):
    return db.query(MK).filter_by(kode=kode).first()


def create(db: Session, data: MKCreate):
    obj = MK(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, mk_id: int, data: MKUpdate):
    obj = get(db, mk_id)
    if not obj:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, mk_id: int):
    if db.query(Kelas).filter_by(mk_id=mk_id).count() > 0:
        return None
    obj = get(db, mk_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj


# ============ PEMETAAN ============

def map_cpmk_mk(db: Session, cpmk_id: int, mk_id: int):
    cpmk = db.query(CPMK).get(cpmk_id)
    mk = db.query(MK).get(mk_id)
    if not cpmk or not mk:
        return None
    if mk not in cpmk.mk_list:
        cpmk.mk_list.append(mk)
        db.commit()
    return True


def unmap_cpmk_mk(db: Session, cpmk_id: int, mk_id: int):
    cpmk = db.query(CPMK).get(cpmk_id)
    mk = db.query(MK).get(mk_id)
    if cpmk and mk and mk in cpmk.mk_list:
        cpmk.mk_list.remove(mk)
        db.commit()
    return True


def get_pemetaan(db: Session, mk_id: int = None, cpmk_id: int = None):
    """List pemetaan CPMK-MK (bisa filter)."""
    q = db.query(CPMK)
    if cpmk_id:
        q = q.filter(CPMK.id == cpmk_id)
    hasil = []
    for cpmk in q.all():
        for mk in cpmk.mk_list:
            if mk_id and mk.id != mk_id:
                continue
            hasil.append({
                "cpmk_id": cpmk.id, "cpmk_kode": cpmk.kode,
                "cpmk_deskripsi": cpmk.deskripsi[:60],
                "mk_id": mk.id, "mk_kode": mk.kode, "mk_nama": mk.nama,
            })
    return hasil