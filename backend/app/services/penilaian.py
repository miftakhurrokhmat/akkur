"""
Service kalkulasi nilai:
    nilai_komponen → nilai_CPMK → nilai_MK → ketercapaian_CPL

Rumus sesuai file HTML 19 & 20.
"""
from decimal import Decimal
from sqlalchemy.orm import Session
from ..models.penilaian import (
    NilaiKomponen, NilaiCPMK, NilaiMK,
    BobotCPMKMK, KonfigurasiPenilaianCPMK,
)
from ..models.krs import KRSDetail
from ..models.kurikulum import MK, CPMK
from ..crud import nilai as crud_nilai
from ..utils.konversi_nilai import angka_ke_huruf


# ============================================================
# STEP 1: HITUNG NILAI CPMK
# ============================================================
def hitung_nilai_cpmk(db: Session, krs_detail_id: int) -> dict:
    """
    Nilai CPMK = Σ (nilai_komponen × bobot_komponen_dalam_CPMK) / Σ bobot

    Bobot per komponen di CPMK diambil dari `konfigurasi_penilaian_cpmk`.
    Jika tidak ada konfigurasi, fallback ke bobot_komponen_mk.
    """
    kd = db.query(KRSDetail).get(krs_detail_id)
    if not kd:
        return {}

    kelas_id = kd.kelas_id

    # Ambil CPMK yang terkait dengan MK ini
    bobot_cpmk_list = db.query(BobotCPMKMK).filter_by(kelas_id=kelas_id).all()
    if not bobot_cpmk_list:
        return {}

    hasil = {}
    for bobot_cpmk in bobot_cpmk_list:
        cpmk_id = bobot_cpmk.cpmk_id

        # Ambil konfigurasi per CPMK (partisipasi, UTS, dll)
        konfigurasi = db.query(KonfigurasiPenilaianCPMK).filter_by(
            kelas_id=kelas_id, cpmk_id=cpmk_id
        ).all()

        if konfigurasi:
            total = Decimal("0")
            total_bobot = Decimal("0")
            for cfg in konfigurasi:
                nk = crud_nilai.get_nilai_komponen(db, krs_detail_id, cfg.komponen_id)
                if nk and nk.nilai is not None:
                    total += Decimal(str(nk.nilai)) * Decimal(str(cfg.bobot))
                    total_bobot += Decimal(str(cfg.bobot))
            nilai_cpmk = (total / total_bobot) if total_bobot > 0 else Decimal("0")
        else:
            # Fallback: hitung rata-rata semua nilai komponen yang ada
            semua_nilai = db.query(NilaiKomponen).filter_by(
                krs_detail_id=krs_detail_id
            ).all()
            nilai_ada = [float(n.nilai) for n in semua_nilai if n.nilai is not None]
            nilai_cpmk = (Decimal(str(sum(nilai_ada) / len(nilai_ada)))
                          if nilai_ada else Decimal("0"))

        hasil[cpmk_id] = float(nilai_cpmk)
        crud_nilai.upsert_nilai_cpmk(db, krs_detail_id, cpmk_id, nilai_cpmk)

    return hasil


# ============================================================
# STEP 2: HITUNG NILAI MK
# ============================================================
def hitung_nilai_mk(db: Session, krs_detail_id: int) -> dict:
    """
    Nilai MK = Σ (nilai_CPMK × bobot_CPMK_dalam_MK) / 100
    Sesuai Rumus Tabel 19.
    """
    kd = db.query(KRSDetail).get(krs_detail_id)
    if not kd:
        return {"error": "KRS Detail tidak ditemukan"}

    kelas_id = kd.kelas_id

    # Pastikan nilai CPMK terbaru
    hitung_nilai_cpmk(db, krs_detail_id)

    # Hitung weighted sum
    bobot_cpmk_list = db.query(BobotCPMKMK).filter_by(kelas_id=kelas_id).all()
    if not bobot_cpmk_list:
        return {"error": "Belum ada konfigurasi bobot CPMK"}

    total = Decimal("0")
    for bc in bobot_cpmk_list:
        nc = db.query(NilaiCPMK).filter_by(
            krs_detail_id=krs_detail_id, cpmk_id=bc.cpmk_id
        ).first()
        if nc and nc.nilai is not None:
            total += Decimal(str(nc.nilai)) * Decimal(str(bc.bobot))

    nilai_angka = total / Decimal("100")
    huruf, bobot_nilai, lulus = angka_ke_huruf(float(nilai_angka))

    crud_nilai.upsert_nilai_mk(
        db, krs_detail_id, nilai_angka,
        huruf, float(bobot_nilai), lulus,
    )

    return {
        "nilai_angka": round(float(nilai_angka), 2),
        "nilai_huruf": huruf,
        "bobot": float(bobot_nilai),
        "lulus": lulus,
    }


# ============================================================
# STEP 3: HITUNG KETERCAPAIAN CPL
# ============================================================
def hitung_ketercapaian_cpl(db: Session, mahasiswa_id: int, tahun_id: int) -> list:
    """
    Nilai CPL = Σ (nilai_MK × SKS_MK) / Σ (SKS_MK × 100) × 100
    Sesuai Rumus Tabel 20.
    """
    from ..models.krs import KRS

    details = (
        db.query(KRSDetail)
        .join(KRS)
        .filter(
            KRS.mahasiswa_id == mahasiswa_id,
            KRS.tahun_akademik_id == tahun_id,
            KRS.status == "disetujui",
        )
        .all()
    )

    by_cpl = {}
    for d in details:
        nm = db.query(NilaiMK).filter_by(krs_detail_id=d.id).first()
        if not nm or nm.nilai_angka is None:
            continue
        sks = d.kelas.mk.sks
        # Setiap CPMK MK punya cpl_id
        cpl_ids = set(c.cpl_id for c in d.kelas.mk.cpmk_list)
        for cpl_id in cpl_ids:
            entry = by_cpl.setdefault(cpl_id, {"skor_maks": 0, "total": 0})
            entry["skor_maks"] += sks * 100
            entry["total"] += float(nm.nilai_angka) * sks

    hasil = []
    for cpl_id, v in by_cpl.items():
        if v["skor_maks"] == 0:
            continue
        rata = (v["total"] / v["skor_maks"]) * 100
        status = "tercapai" if rata >= 60 else "belum"
        hasil.append({
            "cpl_id": cpl_id,
            "skor_maks": v["skor_maks"],
            "total": round(v["total"], 2),
            "nilai_rata_rata": round(rata, 2),
            "status": status,
        })
        crud_nilai.upsert_ketercapaian(
            db, mahasiswa_id, cpl_id, tahun_id,
            v["skor_maks"], v["total"], rata, status,
        )

    return hasil