from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.kurikulum import CPLCreate, CPLUpdate, CPLOut
from ..crud import cpl as crud
from ..core.deps import require_role

router = APIRouter(prefix="/api/cpl", tags=["Master - CPL"])


@router.get("", response_model=list[CPLOut])
def list_cpl(
    skip: int = 0, limit: int = Query(100, le=500),
    aspek: str = None,
    db: Session = Depends(get_db),
):
    return crud.list(db, skip=skip, limit=limit, aspek=aspek)


@router.get("/{cpl_id}", response_model=CPLOut)
def detail_cpl(cpl_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, cpl_id)
    if not obj:
        raise HTTPException(404, "CPL tidak ditemukan")
    return obj


@router.post("", response_model=CPLOut, status_code=201)
def create_cpl(
    data: CPLCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    if crud.get_by_kode(db, data.kode):
        raise HTTPException(400, f"Kode CPL {data.kode} sudah ada")
    return crud.create(db, data)


@router.put("/{cpl_id}", response_model=CPLOut)
def update_cpl(
    cpl_id: int, data: CPLUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    if crud.get(db, cpl_id) is None:
        raise HTTPException(404, "CPL tidak ditemukan")
    if data.kode and data.kode != crud.get(db, cpl_id).kode:
        if crud.get_by_kode(db, data.kode):
            raise HTTPException(400, f"Kode {data.kode} sudah dipakai")
    return crud.update(db, cpl_id, data)


@router.delete("/{cpl_id}", status_code=204)
def delete_cpl(
    cpl_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    if crud.get(db, cpl_id) is None:
        raise HTTPException(404, "CPL tidak ditemukan")
    if crud.is_used(db, cpl_id):
        raise HTTPException(400, "CPL masih dipakai CPMK, tidak bisa dihapus")
    crud.delete(db, cpl_id)