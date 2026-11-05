from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.akademik import KelasCreate, KelasUpdate, KelasOut
from ..crud import kelas as crud
from ..core.deps import require_role

router = APIRouter(prefix="/api/kelas", tags=["Akademik - Kelas"])


@router.get("")
def list_kelas(
    tahun_id: int = None, mk_id: int = None, dosen_id: int = None,
    skip: int = 0, limit: int = Query(200, le=500),
    db: Session = Depends(get_db),
):
    rows = crud.list(db, tahun_id=tahun_id, mk_id=mk_id,
                     dosen_id=dosen_id, skip=skip, limit=limit)
    return [
        {
            "id": k.id, "kode_kelas": k.kode_kelas,
            "mk_id": k.mk_id, "mk_kode": k.mk.kode, "mk_nama": k.mk.nama,
            "sks": k.mk.sks, "semester": k.mk.semester,
            "tahun_akademik_id": k.tahun_akademik_id,
            "tahun_kode": k.tahun_akademik.kode,
            "dosen_id": k.dosen_id,
            "dosen_nama": k.dosen.nama if k.dosen else None,
            "kapasitas": k.kapasitas,
            "terisi": crud.jumlah_peserta(db, k.id),
            "jadwal": k.jadwal, "ruang": k.ruang,
        }
        for k in rows
    ]


@router.get("/{kelas_id}", response_model=KelasOut)
def detail_kelas(kelas_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, kelas_id)
    if not obj:
        raise HTTPException(404, "Kelas tidak ditemukan")
    return obj


@router.get("/{kelas_id}/peserta")
def peserta_kelas(kelas_id: int, db: Session = Depends(get_db)):
    from ..models.krs import KRSDetail
    obj = crud.get(db, kelas_id)
    if not obj:
        raise HTTPException(404, "Kelas tidak ditemukan")
    details = db.query(KRSDetail).filter_by(
        kelas_id=kelas_id, status="aktif"
    ).all()
    return [
        {
            "krs_detail_id": d.id,
            "nim": d.krs.mahasiswa.nim,
            "nama": d.krs.mahasiswa.nama,
            "angkatan": d.krs.mahasiswa.angkatan,
        }
        for d in details
    ]


@router.post("", response_model=KelasOut, status_code=201)
def create_kelas(
    data: KelasCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    existing = crud.get_by_kode(
        db, data.mk_id, data.tahun_akademik_id, data.kode_kelas
    )
    if existing:
        raise HTTPException(400, f"Kelas {data.kode_kelas} sudah ada")
    return crud.create(db, data)


@router.put("/{kelas_id}", response_model=KelasOut)
def update_kelas(
    kelas_id: int, data: KelasUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    if crud.get(db, kelas_id) is None:
        raise HTTPException(404, "Kelas tidak ditemukan")
    return crud.update(db, kelas_id, data)


@router.delete("/{kelas_id}", status_code=204)
def delete_kelas(
    kelas_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    if crud.get(db, kelas_id) is None:
        raise HTTPException(404, "Kelas tidak ditemukan")
    if crud.delete(db, kelas_id) is None:
        raise HTTPException(400, "Kelas masih punya peserta KRS")