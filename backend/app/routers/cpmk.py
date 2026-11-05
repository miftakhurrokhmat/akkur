from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.kurikulum import CPMKCreate, CPMKUpdate, CPMKOut
from ..crud import cpmk as crud
from ..core.deps import require_role

router = APIRouter(prefix="/api/cpmk", tags=["Master - CPMK"])


@router.get("", response_model=list[CPMKOut])
def list_cpmk(
    skip: int = 0, limit: int = Query(200, le=500),
    cpl_id: int = None,
    db: Session = Depends(get_db),
):
    return crud.list(db, skip=skip, limit=limit, cpl_id=cpl_id)


@router.get("/{cpmk_id}", response_model=CPMKOut)
def detail_cpmk(cpmk_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, cpmk_id)
    if not obj:
        raise HTTPException(404, "CPMK tidak ditemukan")
    return obj


@router.post("", response_model=CPMKOut, status_code=201)
def create_cpmk(
    data: CPMKCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    if crud.get_by_kode(db, data.kode):
        raise HTTPException(400, f"Kode CPMK {data.kode} sudah ada")
    return crud.create(db, data)


@router.put("/{cpmk_id}", response_model=CPMKOut)
def update_cpmk(
    cpmk_id: int, data: CPMKUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    if crud.get(db, cpmk_id) is None:
        raise HTTPException(404, "CPMK tidak ditemukan")
    return crud.update(db, cpmk_id, data)


@router.delete("/{cpmk_id}", status_code=204)
def delete_cpmk(
    cpmk_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    if crud.get(db, cpmk_id) is None:
        raise HTTPException(404, "CPMK tidak ditemukan")
    if crud.is_used(db, cpmk_id):
        raise HTTPException(400, "CPMK masih dipakai Sub-CPMK/MK")
    crud.delete(db, cpmk_id)