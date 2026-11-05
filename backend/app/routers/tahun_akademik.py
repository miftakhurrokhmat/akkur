from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.akademik import (
    TahunAkademikCreate, TahunAkademikUpdate, TahunAkademikOut
)
from ..crud import tahun_akademik as crud
from ..core.deps import require_role

router = APIRouter(prefix="/api/tahun-akademik",
                   tags=["Akademik - Tahun Akademik"])


@router.get("", response_model=list[TahunAkademikOut])
def list_ta(aktif_only: bool = False, db: Session = Depends(get_db)):
    return crud.list(db, aktif_only=aktif_only)


@router.get("/aktif", response_model=TahunAkademikOut)
def ta_aktif(db: Session = Depends(get_db)):
    obj = crud.get_aktif(db)
    if not obj:
        raise HTTPException(404, "Belum ada tahun akademik aktif")
    return obj


@router.get("/{ta_id}", response_model=TahunAkademikOut)
def detail_ta(ta_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, ta_id)
    if not obj:
        raise HTTPException(404, "Tahun akademik tidak ditemukan")
    return obj


@router.post("", response_model=TahunAkademikOut, status_code=201)
def create_ta(
    data: TahunAkademikCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    return crud.create(db, data)


@router.put("/{ta_id}", response_model=TahunAkademikOut)
def update_ta(
    ta_id: int, data: TahunAkademikUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    if crud.get(db, ta_id) is None:
        raise HTTPException(404, "Tahun akademik tidak ditemukan")
    return crud.update(db, ta_id, data)


@router.delete("/{ta_id}", status_code=204)
def delete_ta(
    ta_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    if crud.get(db, ta_id) is None:
        raise HTTPException(404, "Tahun akademik tidak ditemukan")
    if crud.delete(db, ta_id) is None:
        raise HTTPException(400, "Tahun akademik masih punya kelas")