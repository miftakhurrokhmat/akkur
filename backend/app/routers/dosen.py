from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.akademik import DosenCreate, DosenUpdate, DosenOut
from ..crud import dosen as crud
from ..core.deps import require_role

router = APIRouter(prefix="/api/dosen", tags=["Akademik - Dosen"])


@router.get("", response_model=list[DosenOut])
def list_dosen(
    skip: int = 0, limit: int = Query(100, le=500),
    db: Session = Depends(get_db),
):
    return crud.list(db, skip=skip, limit=limit)


@router.get("/{dosen_id}", response_model=DosenOut)
def detail_dosen(dosen_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, dosen_id)
    if not obj:
        raise HTTPException(404, "Dosen tidak ditemukan")
    return obj


@router.post("", response_model=DosenOut, status_code=201)
def create_dosen(
    data: DosenCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    if crud.get_by_nidn(db, data.nidn):
        raise HTTPException(400, f"NIDN {data.nidn} sudah ada")
    return crud.create(db, data)


@router.put("/{dosen_id}", response_model=DosenOut)
def update_dosen(
    dosen_id: int, data: DosenUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    if crud.get(db, dosen_id) is None:
        raise HTTPException(404, "Dosen tidak ditemukan")
    return crud.update(db, dosen_id, data)


@router.delete("/{dosen_id}", status_code=204)
def delete_dosen(
    dosen_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    if crud.get(db, dosen_id) is None:
        raise HTTPException(404, "Dosen tidak ditemukan")
    if crud.delete(db, dosen_id) is None:
        raise HTTPException(400, "Dosen masih mengampu kelas")