from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.kurikulum import SubCPMKCreate, SubCPMKUpdate, SubCPMKOut
from ..crud import sub_cpmk as crud
from ..core.deps import require_role

router = APIRouter(prefix="/api/sub-cpmk", tags=["Master - SubCPMK"])


@router.get("", response_model=list[SubCPMKOut])
def list_sub(
    skip: int = 0, limit: int = Query(500, le=1000),
    cpmk_id: int = None,
    db: Session = Depends(get_db),
):
    return crud.list(db, skip=skip, limit=limit, cpmk_id=cpmk_id)


@router.get("/{sub_id}", response_model=SubCPMKOut)
def detail_sub(sub_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, sub_id)
    if not obj:
        raise HTTPException(404, "Sub-CPMK tidak ditemukan")
    return obj


@router.post("", response_model=SubCPMKOut, status_code=201)
def create_sub(
    data: SubCPMKCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    return crud.create(db, data)


@router.put("/{sub_id}", response_model=SubCPMKOut)
def update_sub(
    sub_id: int, data: SubCPMKUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    if crud.get(db, sub_id) is None:
        raise HTTPException(404, "Sub-CPMK tidak ditemukan")
    return crud.update(db, sub_id, data)


@router.delete("/{sub_id}", status_code=204)
def delete_sub(
    sub_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    if crud.get(db, sub_id) is None:
        raise HTTPException(404, "Sub-CPMK tidak ditemukan")
    crud.delete(db, sub_id)