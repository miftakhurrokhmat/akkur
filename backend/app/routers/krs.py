from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.krs import KRSCreate, KRSDetailCreate, KRSOut
from ..crud import krs as crud, mahasiswa as crud_mhs, kelas as crud_kelas
from ..services import krs_service
from ..core.deps import require_role, get_current_user
from ..models.auth import User

router = APIRouter(prefix="/api/krs", tags=["Transaksi - KRS"])


@router.post("", response_model=KRSOut, status_code=201)
def buat_krs(
    data: KRSCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin", "mahasiswa")),
):
    if not crud_mhs.get(db, data.mahasiswa_id):
        raise HTTPException(404, "Mahasiswa tidak ditemukan")
    if crud.get_by_mhs_tahun(db, data.mahasiswa_id, data.tahun_akademik_id):
        raise HTTPException(400, "KRS sudah ada untuk semester ini")
    return crud.create(db, data)


@router.get("/mahasiswa/{mhs_id}")
def list_krs_mhs(mhs_id: int, db: Session = Depends(get_db)):
    if not crud_mhs.get(db, mhs_id):
        raise HTTPException(404, "Mahasiswa tidak ditemukan")
    krs_list = crud.list_by_mahasiswa(db, mhs_id)
    return [
        {
            "id": k.id, "tahun_akademik_id": k.tahun_akademik_id,
            "tahun_kode": k.tahun_akademik.kode,
            "status": k.status, "total_sks": k.total_sks,
            "tanggal_isi": k.tanggal_isi,
            "jumlah_mk": len(k.detail_list),
        }
        for k in krs_list
    ]


@router.get("/{krs_id}")
def detail_krs(krs_id: int, db: Session = Depends(get_db)):
    krs = crud.get(db, krs_id)
    if not krs:
        raise HTTPException(404, "KRS tidak ditemukan")
    return {
        "id": krs.id,
        "mahasiswa": krs.mahasiswa.nama,
        "nim": krs.mahasiswa.nim,
        "tahun_akademik_id": krs.tahun_akademik_id,
        "tahun_kode": krs.tahun_akademik.kode,
        "status": krs.status,
        "total_sks": krs.total_sks,
        "tanggal_isi": krs.tanggal_isi,
        "detail": [
            {
                "id": d.id,
                "kelas_id": d.kelas_id,
                "kode_kelas": d.kelas.kode_kelas,
                "mk_kode": d.kelas.mk.kode,
                "mk_nama": d.kelas.mk.nama,
                "sks": d.kelas.mk.sks,
                "dosen": d.kelas.dosen.nama if d.kelas.dosen else None,
                "status": d.status,
            }
            for d in krs.detail_list
        ],
    }


@router.post("/{krs_id}/detail", status_code=201)
def tambah_detail(
    krs_id: int, data: KRSDetailCreate,
    db: Session = Depends(get_db),
):
    krs = crud.get(db, krs_id)
    if not krs:
        raise HTTPException(404, "KRS tidak ditemukan")
    kelas = crud_kelas.get(db, data.kelas_id)
    if not kelas:
        raise HTTPException(404, "Kelas tidak ditemukan")

    err = krs_service.validasi_tambah_kelas(db, krs, kelas)
    if err:
        raise HTTPException(400, err)

    detail = crud.tambah_detail(db, krs_id, data)
    return {"id": detail.id, "total_sks": detail.krs.total_sks}


@router.delete("/detail/{detail_id}", status_code=204)
def hapus_detail(detail_id: int, db: Session = Depends(get_db)):
    from ..models.krs import KRSDetail
    d = db.query(KRSDetail).get(detail_id)
    if not d:
        raise HTTPException(404, "Detail tidak ditemukan")
    if d.krs.status != "draft":
        raise HTTPException(400, f"KRS berstatus {d.krs.status}")
    crud.hapus_detail(db, detail_id)


@router.post("/{krs_id}/ajukan")
def ajukan(krs_id: int, db: Session = Depends(get_db)):
    krs = crud.get(db, krs_id)
    if not krs:
        raise HTTPException(404, "KRS tidak ditemukan")
    err = krs_service.validasi_ajukan(krs)
    if err:
        raise HTTPException(400, err)
    crud.ajukan(db, krs_id)
    return {"status": "diajukan", "total_sks": krs.total_sks}


@router.post("/{krs_id}/setujui")
def setujui(
    krs_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("dosen", "admin")),
):
    krs = crud.get(db, krs_id)
    if not krs:
        raise HTTPException(404, "KRS tidak ditemukan")
    err = krs_service.validasi_setujui(krs)
    if err:
        raise HTTPException(400, err)
    dosen_id = user.ref_id or 1
    crud.setujui(db, krs_id, dosen_id)
    return {"status": "disetujui", "approved_at": str(krs.approved_at)}


@router.post("/{krs_id}/tolak")
def tolak(
    krs_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("dosen", "admin")),
):
    krs = crud.get(db, krs_id)
    if not krs:
        raise HTTPException(404, "KRS tidak ditemukan")
    if krs.status != "diajukan":
        raise HTTPException(400, f"KRS berstatus {krs.status}")
    crud.tolak(db, krs_id)
    return {"status": "ditolak"}