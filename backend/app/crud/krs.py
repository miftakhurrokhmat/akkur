from datetime import date, datetime
from sqlalchemy.orm import Session
from ..models.krs import KRS, KRSDetail
from ..models.akademik import Mahasiswa, Kelas, TahunAkademik
from ..schemas.krs import KRSCreate, KRSDetailCreate


def get(db: Session, krs_id: int):
    return db.query(KRS).get(krs_id)


def get_by_mhs_tahun(db: Session, mhs_id: int, tahun_id: int):
    return db.query(KRS).filter_by(
        mahasiswa_id=mhs_id, tahun_akademik_id=tahun_id
    ).first()


def list_by_mahasiswa(db: Session, mhs_id: int):
    return db.query(KRS).filter_by(mahasiswa_id=mhs_id).order_by(
        KRS.tahun_akademik_id.desc()
    ).all()


def list_by_tahun(db: Session, tahun_id: int, status: str = None):
    q = db.query(KRS).filter_by(tahun_akademik_id=tahun_id)
    if status:
        q = q.filter(KRS.status == status)
    return q.all()


def create(db: Session, data: KRSCreate):
    obj = KRS(
        mahasiswa_id=data.mahasiswa_id,
        tahun_akademik_id=data.tahun_akademik_id,
        tanggal_isi=date.today(),
        status="draft",
        total_sks=0,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def tambah_detail(db: Session, krs_id: int, data: KRSDetailCreate):
    krs = get(db, krs_id)
    if not krs:
        return None
    kelas = db.query(Kelas).get(data.kelas_id)
    if not kelas:
        return None

    detail = KRSDetail(krs_id=krs_id, kelas_id=data.kelas_id, status="aktif")
    db.add(detail)
    db.flush()
    krs.total_sks = sum(d.kelas.mk.sks for d in krs.detail_list)
    db.commit()
    db.refresh(detail)
    return detail


def hapus_detail(db: Session, detail_id: int):
    d = db.query(KRSDetail).get(detail_id)
    if not d:
        return None
    krs = d.krs
    db.delete(d)
    db.flush()
    db.refresh(krs)
    krs.total_sks = sum(x.kelas.mk.sks for x in krs.detail_list)
    db.commit()
    return krs


def ajukan(db: Session, krs_id: int):
    krs = get(db, krs_id)
    if not krs:
        return None
    krs.status = "diajukan"
    db.commit()
    db.refresh(krs)
    return krs


def setujui(db: Session, krs_id: int, dosen_id: int):
    krs = get(db, krs_id)
    if not krs:
        return None
    krs.status = "disetujui"
    krs.approved_by = dosen_id
    krs.approved_at = datetime.now()
    db.commit()
    db.refresh(krs)
    return krs


def tolak(db: Session, krs_id: int):
    krs = get(db, krs_id)
    if not krs:
        return None
    krs.status = "ditolak"
    db.commit()
    db.refresh(krs)
    return krs