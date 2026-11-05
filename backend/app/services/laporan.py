"""
Service untuk 6 laporan sesuai file HTML 19 & 20.
"""
from decimal import Decimal
from sqlalchemy.orm import Session
from ..models.kurikulum import CPL, CPMK, MK
from ..models.akademik import Mahasiswa, Kelas
from ..models.krs import KRS, KRSDetail
from ..models.penilaian import (
    NilaiCPMK, NilaiMK, BobotCPMKMK, KetercapaianCPL,
)


# ============================================================
# LAPORAN 1: Tabel 19 — Rumusan Akhir MK per Kelas
# ============================================================
def laporan_rumusan_mk(db: Session, kelas_id: int) -> dict:
    """
    Tabel 19: MK | CPL | CPMK | Skor Maks | Total
    Menampilkan nilai per CPMK dan nilai akhir MK untuk semua mahasiswa di kelas.
    """
    kelas = db.query(Kelas).get(kelas_id)
    if not kelas:
        return {"error": "Kelas tidak ditemukan"}

    cpmk_list = (
        db.query(CPMK)
        .join(BobotCPMKMK, BobotCPMKMK.cpmk_id == CPMK.id)
        .filter(BobotCPMKMK.kelas_id == kelas_id)
        .all()
    )

    details = db.query(KRSDetail).filter_by(
        kelas_id=kelas_id, status="aktif"
    ).all()

    rows = []
    for d in details:
        mhs = d.krs.mahasiswa
        cpmk_nilai = {}
        for cpmk in cpmk_list:
            nc = db.query(NilaiCPMK).filter_by(
                krs_detail_id=d.id, cpmk_id=cpmk.id
            ).first()
            cpmk_nilai[cpmk.kode] = float(nc.nilai) if nc and nc.nilai else None

        nm = db.query(NilaiMK).filter_by(krs_detail_id=d.id).first()
        rows.append({
            "nim": mhs.nim,
            "nama": mhs.nama,
            "cpmk_nilai": cpmk_nilai,
            "nilai_angka": float(nm.nilai_angka) if nm and nm.nilai_angka else None,
            "nilai_huruf": nm.nilai_huruf if nm else None,
            "bobot": float(nm.bobot_nilai) if nm and nm.bobot_nilai else None,
            "lulus": nm.lulus if nm else False,
        })

    return {
        "kelas": kelas.kode_kelas,
        "mk": kelas.mk.nama,
        "sks": kelas.mk.sks,
        "dosen": kelas.dosen.nama if kelas.dosen else None,
        "cpmk_kolom": [c.kode for c in cpmk_list],
        "mahasiswa": rows,
    }


# ============================================================
# LAPORAN 2: Tabel 20 — Rumusan Akhir CPL per Mahasiswa
# ============================================================
def laporan_rumusan_cpl(db: Session, mahasiswa_id: int, tahun_id: int) -> dict:
    """
    Tabel 20: CPL | MK | CPMK | Skor Maks | Total
    """
    mhs = db.query(Mahasiswa).get(mahasiswa_id)
    if not mhs:
        return {"error": "Mahasiswa tidak ditemukan"}

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
        cpl_ids = set(c.cpl_id for c in d.kelas.mk.cpmk_list)
        for cpl_id in cpl_ids:
            entry = by_cpl.setdefault(cpl_id, {
                "skor_maks": 0, "total": 0, "mk_list": []
            })
            entry["skor_maks"] += sks * 100
            entry["total"] += float(nm.nilai_angka) * sks
            entry["mk_list"].append({
                "mk": d.kelas.mk.nama,
                "sks": sks,
                "nilai": float(nm.nilai_angka),
                "nilai_x_sks": round(float(nm.nilai_angka) * sks, 2),
                "skor_maks": sks * 100,
            })

    rows = []
    for cpl_id, v in by_cpl.items():
        cpl = db.query(CPL).get(cpl_id)
        rata = v["total"] / v["skor_maks"] * 100 if v["skor_maks"] else 0
        rows.append({
            "kode": cpl.kode,
            "deskripsi": cpl.deskripsi,
            "skor_maks": v["skor_maks"],
            "total": round(v["total"], 2),
            "nilai": round(rata, 2),
            "status": "tercapai" if rata >= 60 else "belum",
            "mk_detail": v["mk_list"],
        })

    rows.sort(key=lambda x: x["kode"])
    return {
        "mahasiswa": {
            "nim": mhs.nim, "nama": mhs.nama, "angkatan": mhs.angkatan,
        },
        "tahun_id": tahun_id,
        "cpl": rows,
        "ringkasan": {
            "tercapai": sum(1 for r in rows if r["status"] == "tercapai"),
            "belum": sum(1 for r in rows if r["status"] == "belum"),
            "total_cpl": len(rows),
        },
    }


# ============================================================
# LAPORAN 3: Transkrip Nilai Mahasiswa
# ============================================================
def laporan_transkrip(db: Session, mahasiswa_id: int) -> dict:
    mhs = db.query(Mahasiswa).get(mahasiswa_id)
    if not mhs:
        return {"error": "Mahasiswa tidak ditemukan"}

    details = (
        db.query(KRSDetail)
        .join(KRS)
        .filter(
            KRS.mahasiswa_id == mahasiswa_id,
            KRS.status == "disetujui",
        )
        .all()
    )

    rows = []
    total_sks = 0
    total_mutu = 0.0
    for d in details:
        nm = db.query(NilaiMK).filter_by(krs_detail_id=d.id).first()
        if not nm or nm.nilai_angka is None:
            continue
        sks = d.kelas.mk.sks
        mutu = float(nm.bobot_nilai or 0) * sks
        total_sks += sks
        total_mutu += mutu
        rows.append({
            "semester": d.kelas.mk.semester,
            "kode_mk": d.kelas.mk.kode,
            "mk": d.kelas.mk.nama,
            "sks": sks,
            "nilai_angka": float(nm.nilai_angka),
            "nilai_huruf": nm.nilai_huruf,
            "bobot": float(nm.bobot_nilai or 0),
            "mutu": round(mutu, 2),
        })

    rows.sort(key=lambda x: (x["semester"], x["kode_mk"]))
    ipk = total_mutu / total_sks if total_sks else 0

    return {
        "mahasiswa": {
            "nim": mhs.nim, "nama": mhs.nama,
            "angkatan": mhs.angkatan, "prodi": mhs.prodi,
        },
        "nilai": rows,
        "total_sks": total_sks,
        "total_mutu": round(total_mutu, 2),
        "ipk": round(ipk, 2),
    }


# ============================================================
# LAPORAN 4: Distribusi Nilai CPMK per Kelas
# ============================================================
def laporan_distribusi_cpmk(db: Session, kelas_id: int) -> dict:
    kelas = db.query(Kelas).get(kelas_id)
    if not kelas:
        return {"error": "Kelas tidak ditemukan"}

    cpmk_list = (
        db.query(CPMK)
        .join(BobotCPMKMK, BobotCPMKMK.cpmk_id == CPMK.id)
        .filter(BobotCPMKMK.kelas_id == kelas_id)
        .all()
    )

    hasil = []
    for cpmk in cpmk_list:
        nilai_list = [
            float(nc.nilai) for nc in
            db.query(NilaiCPMK)
            .join(KRSDetail)
            .filter(
                KRSDetail.kelas_id == kelas_id,
                NilaiCPMK.cpmk_id == cpmk.id,
                NilaiCPMK.nilai.isnot(None),
            ).all()
        ]
        if not nilai_list:
            continue

        buckets = {"A": 0, "AB": 0, "B": 0, "BC": 0, "C": 0, "D": 0, "E": 0}
        for n in nilai_list:
            if n >= 85: buckets["A"] += 1
            elif n >= 80: buckets["AB"] += 1
            elif n >= 70: buckets["B"] += 1
            elif n >= 65: buckets["BC"] += 1
            elif n >= 55: buckets["C"] += 1
            elif n >= 45: buckets["D"] += 1
            else: buckets["E"] += 1

        hasil.append({
            "kode": cpmk.kode,
            "jumlah_mahasiswa": len(nilai_list),
            "rata_rata": round(sum(nilai_list) / len(nilai_list), 2),
            "min": min(nilai_list),
            "max": max(nilai_list),
            "distribusi": buckets,
        })

    return {
        "kelas": kelas.kode_kelas,
        "mk": kelas.mk.nama,
        "cpmk": hasil,
    }


# ============================================================
# LAPORAN 5: CPL Prodi (Agregasi semua mahasiswa)
# ============================================================
def laporan_cpl_prodi(db: Session, prodi: str, tahun_id: int) -> dict:
    mahasiswa_list = db.query(Mahasiswa).filter_by(prodi=prodi).all()
    semua_cpl = {}

    for mhs in mahasiswa_list:
        result = laporan_rumusan_cpl(db, mhs.id, tahun_id)
        for cpl in result.get("cpl", []):
            key = cpl["kode"]
            entry = semua_cpl.setdefault(key, {
                "deskripsi": cpl["deskripsi"],
                "nilai_list": [],
                "tercapai": 0,
                "belum": 0,
            })
            entry["nilai_list"].append(cpl["nilai"])
            if cpl["status"] == "tercapai":
                entry["tercapai"] += 1
            else:
                entry["belum"] += 1

    rows = []
    for kode, v in sorted(semua_cpl.items()):
        rata = (sum(v["nilai_list"]) / len(v["nilai_list"])
                if v["nilai_list"] else 0)
        rows.append({
            "kode": kode,
            "deskripsi": v["deskripsi"],
            "jumlah_mahasiswa": len(v["nilai_list"]),
            "rata_rata": round(rata, 2),
            "tercapai": v["tercapai"],
            "belum": v["belum"],
        })

    return {
        "prodi": prodi,
        "tahun_id": tahun_id,
        "jumlah_mahasiswa": len(mahasiswa_list),
        "cpl": rows,
    }


# ============================================================
# LAPORAN 6: Rekap KRS per Kelas
# ============================================================
def laporan_krs_kelas(db: Session, kelas_id: int) -> dict:
    kelas = db.query(Kelas).get(kelas_id)
    if not kelas:
        return {"error": "Kelas tidak ditemukan"}

    details = db.query(KRSDetail).filter_by(
        kelas_id=kelas_id, status="aktif"
    ).all()

    return {
        "kelas": kelas.kode_kelas,
        "mk": kelas.mk.nama,
        "kapasitas": kelas.kapasitas,
        "terisi": len(details),
        "sisa": kelas.kapasitas - len(details),
        "peserta": [
            {
                "nim": d.krs.mahasiswa.nim,
                "nama": d.krs.mahasiswa.nama,
                "angkatan": d.krs.mahasiswa.angkatan,
            }
            for d in details
        ],
    }