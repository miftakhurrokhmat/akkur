from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class KRSCreate(BaseModel):
    mahasiswa_id: int
    tahun_akademik_id: int


class KRSDetailCreate(BaseModel):
    kelas_id: int


class KRSDetailOut(BaseModel):
    id: int
    kelas_id: int
    status: str
    class Config:
        from_attributes = True


class KRSOut(BaseModel):
    id: int
    mahasiswa_id: int
    tahun_akademik_id: int
    tanggal_isi: Optional[date] = None
    status: str
    total_sks: int
    approved_at: Optional[datetime] = None
    class Config:
        from_attributes = True