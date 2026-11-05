from sqlalchemy.orm import Session
from ..models.akademik import TahunAkademik, Kelas
from ..schemas.akademik import TahunAkademikCreate, TahunAkademikUpdate


def list(db: Session, aktif_only: bool = False):
    q = db.query(TahunAkademik)
    if aktif_only:
        q = q.filter(TahunAkademik.aktif == True)
    return q.order_by(TahunAkademik.tahun_mulai.desc(),
                      TahunAkademik.semester).all()


def get(db: Session, ta_id: int):
    return db.query(TahunAkademik).get(ta_id)


def get_aktif(db: Session):
    return db.query(TahunAkademik).filter_by(aktif=True).first()


def create(db: Session, data: TahunAkademikCreate):
    # Jika set aktif, nonaktifkan yang lain
    if data.aktif:
        db.query(TahunAkademik).update({TahunAkademik.aktif: False})
    obj = TahunAkademik(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, ta_id: int, data: TahunAkademikUpdate):
    obj = get(db, ta_id)
    if not obj:
        return None
    if data.aktif is True:
        db.query(TahunAkademik).filter(TahunAkademik.id != ta_id).update(
            {TahunAkademik.aktif: False}
        )
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, ta_id: int):
    if db.query(Kelas).filter_by(tahun_akademik_id=ta_id).count() > 0:
        return None
    obj = get(db, ta_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj