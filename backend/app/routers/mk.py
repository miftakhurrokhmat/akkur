from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.kurikulum import MKCreate, MKUpdate, MKOut
from ..crud import mk as crud
from ..core.deps import require_role

router = APIRouter(prefix="/api/mk", tags=["Master - MK"])


@router.get("", response_model=list[MKOut])
def list_mk(
    skip: int = 0, limit: int = Query(100, le=500),
    semester: int = None,
    db: Session = Depends(get_db),
):
    return crud.list(db, semester=semester, skip=skip, limit=limit)


@router.get("/{mk_id}", response_model=MKOut)
def detail_mk(mk_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, mk_id)
    if not obj:
        raise HTTPException(404, "MK tidak ditemukan")
    return obj


@router.post("", response_model=MKOut, status_code=201)
def create_mk(
    data: MKCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    if crud.get_by_kode(db, data.kode):
        raise HTTPException(400, f"Kode MK {data.kode} sudah ada")
    return crud.create(db, data)


@router.put("/{mk_id}", response_model=MKOut)
def update_mk(
    mk_id: int, data: MKUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    if crud.get(db, mk_id) is None:
        raise HTTPException(404, "MK tidak ditemukan")
    return crud.update(db, mk_id, data)


@router.delete("/{mk_id}", status_code=204)
def delete_mk(
    mk_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    if crud.get(db, mk_id) is None:
        raise HTTPException(404, "MK tidak ditemukan")
    if crud.delete(db, mk_id) is None:
        raise HTTPException(400, "MK masih dipakai kelas")