from sqlalchemy.orm import Session
from ..models.kurikulum import SubCPMK
from ..schemas.kurikulum import SubCPMKCreate, SubCPMKUpdate


def list(db: Session, skip: int = 0, limit: int = 500, cpmk_id: int = None):
    q = db.query(SubCPMK)
    if cpmk_id:
        q = q.filter(SubCPMK.cpmk_id == cpmk_id)
    return q.order_by(SubCPMK.cpmk_id, SubCPMK.kode).offset(skip).limit(limit).all()


def get(db: Session, sub_id: int):
    return db.query(SubCPMK).get(sub_id)


def create(db: Session, data: SubCPMKCreate):
    obj = SubCPMK(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, sub_id: int, data: SubCPMKUpdate):
    obj = get(db, sub_id)
    if not obj:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, sub_id: int):
    obj = get(db, sub_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj