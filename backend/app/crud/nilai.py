from sqlalchemy.orm import Session
from ..models.penilaian import (
    KomponenPenilaian, BobotKomponenMK, BobotCPMKMK,
    KonfigurasiPenilaianCPMK, NilaiKomponen, NilaiCPMK,
    NilaiMK, KetercapaianCPL,
)


# ============ KOMPONEN PENILAIAN ============
def list_komponen(db: Session, aktif_only: bool = True):
    q = db.query(KomponenPenilaian)
    if aktif_only:
        q = q.filter(KomponenPenilaian.aktif == True)
    return q.order_by(KomponenPenilaian.id).all()


def get_komponen_by_kode(db: Session, kode: str):
    return db.query(KomponenPenilaian).filter_by(kode=kode).first()


# ============ BOBOT KOMPONEN MK ============
def list_bobot_komponen(db: Session, kelas_id: int):
    return db.query(BobotKomponenMK).filter_by(kelas_id=kelas_id).all()


def set_bobot_komponen(db: Session, kelas_id: int, items: list):
    """Replace semua bobot komponen kelas. items = [{komponen_id, bobot}]"""
    db.query(BobotKomponenMK).filter_by(kelas_id=kelas_id).delete()
    for item in items:
        db.add(BobotKomponenMK(
            kelas_id=kelas_id,
            komponen_id=item["komponen_id"],
            bobot=item["bobot"],
        ))
    db.commit()
    return list_bobot_komponen(db, kelas_id)


# ============ BOBOT CPMK MK ============
def list_bobot_cpmk(db: Session, kelas_id: int):
    return db.query(BobotCPMKMK).filter_by(kelas_id=kelas_id).all()


def set_bobot_cpmk(db: Session, kelas_id: int, items: list):
    db.query(BobotCPMKMK).filter_by(kelas_id=kelas_id).delete()
    for item in items:
        db.add(BobotCPMKMK(
            kelas_id=kelas_id,
            cpmk_id=item["cpmk_id"],
            bobot=item["bobot"],
        ))
    db.commit()
    return list_bobot_cpmk(db, kelas_id)


# ============ KONFIGURASI PENILAIAN CPMK ============
def list_konfigurasi(db: Session, kelas_id: int, cpmk_id: int = None):
    q = db.query(KonfigurasiPenilaianCPMK).filter_by(kelas_id=kelas_id)
    if cpmk_id:
        q = q.filter(KonfigurasiPenilaianCPMK.cpmk_id == cpmk_id)
    return q.all()


def set_konfigurasi(db: Session, kelas_id: int, cpmk_id: int, items: list):
    db.query(KonfigurasiPenilaianCPMK).filter_by(
        kelas_id=kelas_id, cpmk_id=cpmk_id
    ).delete()
    for item in items:
        db.add(KonfigurasiPenilaianCPMK(
            kelas_id=kelas_id,
            cpmk_id=cpmk_id,
            komponen_id=item["komponen_id"],
            tahap=item.get("tahap"),
            teknik=item.get("teknik"),
            instrumen=item.get("instrumen"),
            kriteria=item.get("kriteria"),
            bobot=item["bobot"],
        ))
    db.commit()
    return list_konfigurasi(db, kelas_id, cpmk_id)


# ============ NILAI KOMPONEN ============
def get_nilai_komponen(db: Session, krs_detail_id: int, komponen_id: int):
    return db.query(NilaiKomponen).filter_by(
        krs_detail_id=krs_detail_id, komponen_id=komponen_id
    ).first()


def upsert_nilai_komponen(db: Session, krs_detail_id: int, komponen_id: int,
                          nilai: float, dosen_id: int = None, catatan: str = None):
    obj = get_nilai_komponen(db, krs_detail_id, komponen_id)
    if obj:
        obj.nilai = nilai
        obj.catatan = catatan
        obj.updated_by = dosen_id
    else:
        obj = NilaiKomponen(
            krs_detail_id=krs_detail_id,
            komponen_id=komponen_id,
            nilai=nilai,
            catatan=catatan,
            updated_by=dosen_id,
        )
        db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# ============ NILAI CPMK ============
def get_nilai_cpmk(db: Session, krs_detail_id: int, cpmk_id: int):
    return db.query(NilaiCPMK).filter_by(
        krs_detail_id=krs_detail_id, cpmk_id=cpmk_id
    ).first()


def upsert_nilai_cpmk(db: Session, krs_detail_id: int, cpmk_id: int, nilai: float):
    obj = get_nilai_cpmk(db, krs_detail_id, cpmk_id)
    if obj:
        obj.nilai = nilai
    else:
        obj = NilaiCPMK(
            krs_detail_id=krs_detail_id, cpmk_id=cpmk_id, nilai=nilai
        )
        db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# ============ NILAI MK ============
def upsert_nilai_mk(db: Session, krs_detail_id: int, nilai_angka: float,
                    nilai_huruf: str, bobot_nilai: float, lulus: bool):
    obj = db.query(NilaiMK).filter_by(krs_detail_id=krs_detail_id).first()
    if obj:
        obj.nilai_angka = nilai_angka
        obj.nilai_huruf = nilai_huruf
        obj.bobot_nilai = bobot_nilai
        obj.lulus = lulus
    else:
        obj = NilaiMK(
            krs_detail_id=krs_detail_id,
            nilai_angka=nilai_angka,
            nilai_huruf=nilai_huruf,
            bobot_nilai=bobot_nilai,
            lulus=lulus,
        )
        db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# ============ KETERCAPAIAN CPL ============
def upsert_ketercapaian(db: Session, mahasiswa_id: int, cpl_id: int,
                        tahun_id: int, skor_maks: float, total_skor: float,
                        nilai_rata_rata: float, status: str):
    obj = db.query(KetercapaianCPL).filter_by(
        mahasiswa_id=mahasiswa_id, cpl_id=cpl_id, tahun_akademik_id=tahun_id
    ).first()
    if obj:
        obj.skor_maks = skor_maks
        obj.total_skor = total_skor
        obj.nilai_rata_rata = nilai_rata_rata
        obj.status = status
    else:
        obj = KetercapaianCPL(
            mahasiswa_id=mahasiswa_id, cpl_id=cpl_id,
            tahun_akademik_id=tahun_id, skor_maks=skor_maks,
            total_skor=total_skor, nilai_rata_rata=nilai_rata_rata,
            status=status,
        )
        db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj