from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from ..database import get_db
from ..services import laporan as svc
from ..utils import excel_export
from ..core.deps import require_role

router = APIRouter(prefix="/api/laporan", tags=["Laporan"])


@router.get("/rumusan-mk/{kelas_id}")
def rumusan_mk(kelas_id: int, db: Session = Depends(get_db)):
    data = svc.laporan_rumusan_mk(db, kelas_id)
    if "error" in data:
        raise HTTPException(404, data["error"])
    return data


@router.get("/rumusan-cpl/{mahasiswa_id}")
def rumusan_cpl(
    mahasiswa_id: int, tahun_id: int,
    db: Session = Depends(get_db),
):
    data = svc.laporan_rumusan_cpl(db, mahasiswa_id, tahun_id)
    if "error" in data:
        raise HTTPException(404, data["error"])
    return data


@router.get("/transkrip/{mahasiswa_id}")
def transkrip(mahasiswa_id: int, db: Session = Depends(get_db)):
    data = svc.laporan_transkrip(db, mahasiswa_id)
    if "error" in data:
        raise HTTPException(404, data["error"])
    return data


@router.get("/distribusi-cpmk/{kelas_id}")
def distribusi_cpmk(kelas_id: int, db: Session = Depends(get_db)):
    data = svc.laporan_distribusi_cpmk(db, kelas_id)
    if "error" in data:
        raise HTTPException(404, data["error"])
    return data


@router.get("/cpl-prodi")
def cpl_prodi(
    prodi: str, tahun_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin", "dosen")),
):
    return svc.laporan_cpl_prodi(db, prodi, tahun_id)


@router.get("/krs-kelas/{kelas_id}")
def krs_kelas(kelas_id: int, db: Session = Depends(get_db)):
    data = svc.laporan_krs_kelas(db, kelas_id)
    if "error" in data:
        raise HTTPException(404, data["error"])
    return data


# ============ EXPORT EXCEL ============
XLSX_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


@router.get("/export/rumusan-mk/{kelas_id}")
def export_rumusan_mk(kelas_id: int, db: Session = Depends(get_db)):
    data = svc.laporan_rumusan_mk(db, kelas_id)
    if "error" in data:
        raise HTTPException(404, data["error"])
    buf = excel_export.export_rumusan_mk(data)
    return StreamingResponse(
        buf, media_type=XLSX_TYPE,
        headers={"Content-Disposition":
                 f"attachment; filename=rumusan_mk_{kelas_id}.xlsx"},
    )


@router.get("/export/rumusan-cpl/{mahasiswa_id}")
def export_rumusan_cpl(
    mahasiswa_id: int, tahun_id: int,
    db: Session = Depends(get_db),
):
    data = svc.laporan_rumusan_cpl(db, mahasiswa_id, tahun_id)
    if "error" in data:
        raise HTTPException(404, data["error"])
    buf = excel_export.export_rumusan_cpl(data)
    return StreamingResponse(
        buf, media_type=XLSX_TYPE,
        headers={"Content-Disposition":
                 f"attachment; filename=rumusan_cpl_{mahasiswa_id}.xlsx"},
    )


@router.get("/export/transkrip/{mahasiswa_id}")
def export_transkrip(mahasiswa_id: int, db: Session = Depends(get_db)):
    data = svc.laporan_transkrip(db, mahasiswa_id)
    if "error" in data:
        raise HTTPException(404, data["error"])
    buf = excel_export.export_transkrip(data)
    return StreamingResponse(
        buf, media_type=XLSX_TYPE,
        headers={"Content-Disposition":
                 f"attachment; filename=transkrip_{mahasiswa_id}.xlsx"},
    )