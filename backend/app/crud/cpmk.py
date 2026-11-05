from sqlalchemy.orm import Session
from ..models.kurikulum import CPMK, SubCPMK, MK
from ..schemas.kurikulum import CPMKCreate, CPMKUpdate


def list(db: Session, skip: int = 0, limit: int = 200, cpl_id: int = None):
    q = db.query(CPMK)
    if cpl_id:
        q = q.filter(CPMK.cpl_id == cpl_id)
    return q.order_by(CPMK.kode).offset(skip).limit(limit).all()


def get(db: Session, cpmk_id: int):
    return db.query(CPMK).get(cpmk_id)


def get_by_kode(db: Session, kode: str):
    return db.query(CPMK).filter_by(kode=kode).first()


def create(db: Session, data: CPMKCreate):
    obj = CPMK(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, cpmk_id: int, data: CPMKUpdate):
    obj = get(db, cpmk_id)
    if not obj:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, cpmk_id: int):
    obj = get(db, cpmk_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj


def is_used(db: Session, cpmk_id: int) -> bool:
    """Dipakai Sub-CPMK atau MK?"""
    if db.query(SubCPMK).filter_by(cpmk_id=cpmk_id).count() > 0:
        return True
    return db.query(MK).filter(MK.cpmk_list.any(id=cpmk_id)).count() > 0