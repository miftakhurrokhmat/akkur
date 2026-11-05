from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.kurikulum import PemetaanCreate
from ..crud import mk as crud
from ..core.deps import require_role

router = APIRouter(prefix="/api/pemetaan", tags=["Master - Pemetaan CPMK↔MK"])


@router.get("")
def list_pemetaan(
    mk_id: int = None, cpmk_id: int = None,
    db: Session = Depends(get_db),
):
    return crud.get_pemetaan(db, mk_id=mk_id, cpmk_id=cpmk_id)


@router.post("", status_code=201)
def tambah(
    data: PemetaanCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    ok = crud.map_cpmk_mk(db, data.cpmk_id, data.mk_id)
    if not ok:
        raise HTTPException(404, "CPMK atau MK tidak ditemukan")
    return {"status": "ok"}


@router.delete("")
def hapus(
    cpmk_id: int, mk_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    crud.unmap_cpmk_mk(db, cpmk_id, mk_id)
    return {"status": "ok"}