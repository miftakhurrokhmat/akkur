from sqlalchemy.orm import Session
from ..models.kurikulum import CPL, CPMK
from ..schemas.kurikulum import CPLCreate, CPLUpdate


def list(db: Session, skip: int = 0, limit: int = 100, aspek: str = None):
    q = db.query(CPL)
    if aspek:
        q = q.filter(CPL.aspek == aspek)
    return q.order_by(CPL.kode).offset(skip).limit(limit).all()


def get(db: Session, cpl_id: int):
    return db.query(CPL).get(cpl_id)


def get_by_kode(db: Session, kode: str):
    return db.query(CPL).filter_by(kode=kode).first()


def create(db: Session, data: CPLCreate):
    obj = CPL(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, cpl_id: int, data: CPLUpdate):
    obj = get(db, cpl_id)
    if not obj:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, cpl_id: int):
    obj = get(db, cpl_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj


def is_used(db: Session, cpl_id: int) -> bool:
    """Apakah CPL dipakai CPMK?"""
    return db.query(CPMK).filter_by(cpl_id=cpl_id).count() > 0