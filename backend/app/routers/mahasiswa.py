from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.akademik import MahasiswaCreate, MahasiswaUpdate, MahasiswaOut
from ..crud import mahasiswa as crud
from ..core.deps import require_role

router = APIRouter(prefix="/api/mahasiswa", tags=["Akademik - Mahasiswa"])


@router.get("", response_model=list[MahasiswaOut])
def list_mhs(
    skip: int = 0, limit: int = Query(100, le=500),
    angkatan: int = None, prodi: str = None, status: str = None,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin", "dosen")),
):
    return crud.list(db, skip=skip, limit=limit, angkatan=angkatan,
                     prodi=prodi, status=status)


@router.get("/{mhs_id}", response_model=MahasiswaOut)
def detail_mhs(mhs_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, mhs_id)
    if not obj:
        raise HTTPException(404, "Mahasiswa tidak ditemukan")
    return obj


@router.post("", response_model=MahasiswaOut, status_code=201)
def create_mhs(
    data: MahasiswaCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    if crud.get_by_nim(db, data.nim):
        raise HTTPException(400, f"NIM {data.nim} sudah ada")
    return crud.create(db, data)


@router.put("/{mhs_id}", response_model=MahasiswaOut)
def update_mhs(
    mhs_id: int, data: MahasiswaUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    if crud.get(db, mhs_id) is None:
        raise HTTPException(404, "Mahasiswa tidak ditemukan")
    return crud.update(db, mhs_id, data)


@router.delete("/{mhs_id}", status_code=204)
def delete_mhs(
    mhs_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    if crud.get(db, mhs_id) is None:
        raise HTTPException(404, "Mahasiswa tidak ditemukan")
    if crud.delete(db, mhs_id) is None:
        raise HTTPException(400, "Mahasiswa masih punya KRS")