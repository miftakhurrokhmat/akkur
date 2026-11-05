"""
Service validasi KRS.
"""
from sqlalchemy.orm import Session
from ..models.krs import KRS, KRSDetail
from ..models.akademik import Kelas


MIN_SKS = 12
MAX_SKS = 24


def validasi_tambah_kelas(db: Session, krs: KRS, kelas: Kelas) -> str | None:
    """Return error message atau None jika valid."""
    # 1. KRS harus draft
    if krs.status != "draft":
        return f"KRS berstatus {krs.status}, tidak bisa diubah"

    # 2. Kapasitas kelas
    terisi = db.query(KRSDetail).filter_by(
        kelas_id=kelas.id, status="aktif"
    ).count()
    if terisi >= kelas.kapasitas:
        return f"Kelas penuh ({terisi}/{kelas.kapasitas})"

    # 3. Duplikat kelas
    dup = db.query(KRSDetail).filter_by(
        krs_id=krs.id, kelas_id=kelas.id
    ).first()
    if dup:
        return "Kelas sudah ada di KRS"

    # 4. Duplikat MK (tidak boleh ambil 2 kelas MK sama)
    for d in krs.detail_list:
        if d.kelas.mk_id == kelas.mk_id:
            return f"MK {kelas.mk.nama} sudah ada di KRS"

    # 5. Maksimal SKS
    total_baru = krs.total_sks + kelas.mk.sks
    if total_baru > MAX_SKS:
        return f"Melebihi batas {MAX_SKS} SKS (akan jadi {total_baru})"

    return None


def validasi_ajukan(krs: KRS) -> str | None:
    if krs.status != "draft":
        return f"KRS berstatus {krs.status}, tidak bisa diajukan"
    if krs.total_sks < MIN_SKS:
        return f"Minimal {MIN_SKS} SKS, Anda baru {krs.total_sks} SKS"
    if not krs.detail_list:
        return "KRS kosong, tambahkan MK dulu"
    return None


def validasi_setujui(krs: KRS) -> str | None:
    if krs.status != "diajukan":
        return f"KRS berstatus {krs.status}, tidak bisa disetujui"
    return None


def validasi_input_nilai(krs_detail: KRSDetail) -> str | None:
    if krs_detail.krs.status != "disetujui":
        return "KRS belum disetujui, tidak bisa input nilai"
    return None