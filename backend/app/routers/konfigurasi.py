from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.penilaian import (
    SetBobotKomponen, SetBobotCPMK, SetKonfigurasiCPMK,
)
from ..crud import nilai as crud, kelas as crud_kelas
from ..core.deps import require_role

router = APIRouter(prefix="/api/konfigurasi",
                   tags=["Konfigurasi Penilaian"])


def _validasi_sum_100(items, label="bobot"):
    total = sum(float(x.bobot) for x in items)
    if abs(total - 100) > 0.01:
        raise HTTPException(400, f"Total {label} harus 100 (sekarang {total})")


# ============ KOMPONEN PENILAIAN ============
@router.get("/komponen")
def list_komponen(db: Session = Depends(get_db)):
    return [
        {"id": k.id, "kode": k.kode, "nama": k.nama,
         "kategori": k.kategori, "aktif": k.aktif}
        for k in crud.list_komponen(db)
    ]


# ============ BOBOT KOMPONEN MK ============
@router.get("/kelas/{kelas_id}/bobot-komponen")
def get_bobot_komponen(kelas_id: int, db: Session = Depends(get_db)):
    if not crud_kelas.get(db, kelas_id):
        raise HTTPException(404, "Kelas tidak ditemukan")
    rows = crud.list_bobot_komponen(db, kelas_id)
    return [
        {
            "id": b.id, "komponen_id": b.komponen_id,
            "komponen_kode": b.komponen.kode,
            "komponen_nama": b.komponen.nama,
            "bobot": float(b.bobot),
        }
        for b in rows
    ]


@router.post("/kelas/{kelas_id}/bobot-komponen")
def set_bobot_komponen(
    kelas_id: int, data: SetBobotKomponen,
    db: Session = Depends(get_db),
    _=Depends(require_role("dosen", "admin")),
):
    if not crud_kelas.get(db, kelas_id):
        raise HTTPException(404, "Kelas tidak ditemukan")
    _validasi_sum_100(data.items, "bobot komponen")
    items = [{"komponen_id": i.komponen_id, "bobot": i.bobot}
             for i in data.items]
    crud.set_bobot_komponen(db, kelas_id, items)
    return {"status": "ok", "count": len(items)}


# ============ BOBOT CPMK MK ============
@router.get("/kelas/{kelas_id}/bobot-cpmk")
def get_bobot_cpmk(kelas_id: int, db: Session = Depends(get_db)):
    if not crud_kelas.get(db, kelas_id):
        raise HTTPException(404, "Kelas tidak ditemukan")
    rows = crud.list_bobot_cpmk(db, kelas_id)
    return [
        {
            "id": b.id, "cpmk_id": b.cpmk_id,
            "cpmk_kode": b.cpmk.kode,
            "cpmk_deskripsi": b.cpmk.deskripsi[:80],
            "bobot": float(b.bobot),
        }
        for b in rows
    ]


@router.post("/kelas/{kelas_id}/bobot-cpmk")
def set_bobot_cpmk(
    kelas_id: int, data: SetBobotCPMK,
    db: Session = Depends(get_db),
    _=Depends(require_role("dosen", "admin")),
):
    if not crud_kelas.get(db, kelas_id):
        raise HTTPException(404, "Kelas tidak ditemukan")
    _validasi_sum_100(data.items, "bobot CPMK")
    items = [{"cpmk_id": i.cpmk_id, "bobot": i.bobot} for i in data.items]
    crud.set_bobot_cpmk(db, kelas_id, items)
    return {"status": "ok", "count": len(items)}


# ============ KONFIGURASI PER CPMK ============
@router.get("/kelas/{kelas_id}/konfigurasi-cpmk")
def get_konfigurasi(
    kelas_id: int, cpmk_id: int = None,
    db: Session = Depends(get_db),
):
    if not crud_kelas.get(db, kelas_id):
        raise HTTPException(404, "Kelas tidak ditemukan")
    rows = crud.list_konfigurasi(db, kelas_id, cpmk_id)
    return [
        {
            "id": r.id, "cpmk_id": r.cpmk_id,
            "komponen_id": r.komponen_id,
            "komponen_kode": r.komponen.kode,
            "komponen_nama": r.komponen.nama,
            "tahap": r.tahap, "teknik": r.teknik,
            "instrumen": r.instrumen, "kriteria": r.kriteria,
            "bobot": float(r.bobot),
        }
        for r in rows
    ]


@router.post("/kelas/{kelas_id}/konfigurasi-cpmk")
def set_konfigurasi(
    kelas_id: int, data: SetKonfigurasiCPMK,
    db: Session = Depends(get_db),
    _=Depends(require_role("dosen", "admin")),
):
    if not crud_kelas.get(db, kelas_id):
        raise HTTPException(404, "Kelas tidak ditemukan")
    _validasi_sum_100(data.items, "bobot per komponen CPMK")
    items = [
        {
            "komponen_id": i.komponen_id,
            "tahap": i.tahap, "teknik": i.teknik,
            "instrumen": i.instrumen, "kriteria": i.kriteria,
            "bobot": i.bobot,
        }
        for i in data.items
    ]
    crud.set_konfigurasi(db, kelas_id, data.cpmk_id, items)
    return {"status": "ok", "count": len(items)}