from pydantic import BaseModel, Field
from typing import Optional, List


class KomponenPenilaianOut(BaseModel):
    id: int
    kode: str
    nama: str
    kategori: Optional[str] = None
    class Config:
        from_attributes = True


class BobotItem(BaseModel):
    komponen_id: Optional[int] = None
    cpmk_id: Optional[int] = None
    bobot: float = Field(..., ge=0, le=100)


class SetBobotKomponen(BaseModel):
    items: List[BobotItem]


class SetBobotCPMK(BaseModel):
    items: List[BobotItem]


class KonfigurasiItem(BaseModel):
    komponen_id: int
    tahap: Optional[str] = None
    teknik: Optional[str] = None
    instrumen: Optional[str] = None
    kriteria: Optional[str] = None
    bobot: float = Field(..., ge=0, le=100)


class SetKonfigurasiCPMK(BaseModel):
    cpmk_id: int
    items: List[KonfigurasiItem]


class NilaiItem(BaseModel):
    komponen_id: int
    nilai: float = Field(..., ge=0, le=100)
    catatan: Optional[str] = None


class InputNilaiBatch(BaseModel):
    krs_detail_id: int
    dosen_id: int
    items: List[NilaiItem]