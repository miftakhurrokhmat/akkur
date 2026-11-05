from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.penilaian import InputNilaiBatch
from ..crud import nilai as crud
from ..services import penilaian as svc
from ..services import krs_service
from ..core.deps import require_role
from ..models.krs import KRSDetail
from ..models.penilaian import NilaiKomponen, NilaiCPMK

router = APIRouter(prefix="/api/nilai", tags=["Transaksi - Nilai"])


@router.post("/input")
def input_nilai(
    data: InputNilaiBatch,
    db: Session = Depends(get_db),
    _=Depends(require_role("dosen", "admin")),
):
    kd = db.query(KRSDetail).get(data.krs_detail_id)
    if not kd:
        raise HTTPException(404, "KRS Detail tidak ditemukan")

    err = krs_service.validasi_input_nilai(kd)
    if err:
        raise HTTPException(400, err)

    # Upsert nilai komponen
    for item in data.items:
        crud.upsert_nilai_komponen(
            db, data.krs_detail_id, item.komponen_id,
            item.nilai, data.dosen_id, item.catatan,
        )

    # Hitung otomatis
    cpmk_result = svc.hitung_nilai_cpmk(db, data.krs_detail_id)
    mk_result = svc.hitung_nilai_mk(db, data.krs_detail_id)

    return {
        "status": "ok",
        "nilai_cpmk": cpmk_result,
        "nilai_mk": mk_result,
    }


@router.get("/{krs_detail_id}")
def get_nilai(krs_detail_id: int, db: Session = Depends(get_db)):
    kd = db.query(KRSDetail).get(krs_detail_id)
    if not kd:
        raise HTTPException(404, "Tidak ditemukan")

    nilai_komponen = db.query(NilaiKomponen).filter_by(
        krs_detail_id=krs_detail_id
    ).all()
    nilai_cpmk = db.query(NilaiCPMK).filter_by(
        krs_detail_id=krs_detail_id
    ).all()

    return {
        "krs_detail_id": kd.id,
        "mahasiswa": {
            "nim": kd.krs.mahasiswa.nim,
            "nama": kd.krs.mahasiswa.nama,
        },
        "kelas": {
            "kode": kd.kelas.kode_kelas,
            "mk": kd.kelas.mk.nama,
            "sks": kd.kelas.mk.sks,
        },
        "nilai_komponen": [
            {
                "komponen_id": nk.komponen_id,
                "komponen_kode": nk.komponen.kode,
                "komponen_nama": nk.komponen.nama,
                "nilai": float(nk.nilai) if nk.nilai else None,
            }
            for nk in nilai_komponen
        ],
        "nilai_cpmk": [
            {
                "cpmk_id": nc.cpmk_id,
                "cpmk_kode": nc.cpmk.kode,
                "nilai": float(nc.nilai) if nc.nilai else None,
            }
            for nc in nilai_cpmk
        ],
        "nilai_mk": {
            "angka": float(kd.nilai_mk.nilai_angka) if kd.nilai_mk else None,
            "huruf": kd.nilai_mk.nilai_huruf if kd.nilai_mk else None,
            "bobot": float(kd.nilai_mk.bobot_nilai) if kd.nilai_mk else None,
            "lulus": kd.nilai_mk.lulus if kd.nilai_mk else None,
        } if kd.nilai_mk else None,
    }


@router.post("/hitung/{krs_detail_id}")
def hitung_ulang(
    krs_detail_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("dosen", "admin")),
):
    if not db.query(KRSDetail).get(krs_detail_id):
        raise HTTPException(404, "Tidak ditemukan")
    cpmk_result = svc.hitung_nilai_cpmk(db, krs_detail_id)
    mk_result = svc.hitung_nilai_mk(db, krs_detail_id)
    return {
        "status": "ok",
        "nilai_cpmk": cpmk_result,
        "nilai_mk": mk_result,
    }


@router.post("/hitung-cpl/{mahasiswa_id}")
def hitung_cpl(
    mahasiswa_id: int, tahun_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("dosen", "admin")),
):
    hasil = svc.hitung_ketercapaian_cpl(db, mahasiswa_id, tahun_id)
    return {"mahasiswa_id": mahasiswa_id, "ketercapaian_cpl": hasil}