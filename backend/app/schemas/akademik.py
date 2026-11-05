from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date


class MahasiswaBase(BaseModel):
    nim: str = Field(..., max_length=20)
    nama: str = Field(..., max_length=200)
    angkatan: int
    prodi: Optional[str] = None
    status: Optional[str] = "aktif"


class MahasiswaCreate(MahasiswaBase):
    pass


class MahasiswaUpdate(BaseModel):
    nim: Optional[str] = None
    nama: Optional[str] = None
    angkatan: Optional[int] = None
    prodi: Optional[str] = None
    status: Optional[str] = None


class MahasiswaOut(MahasiswaBase):
    id: int
    class Config:
        from_attributes = True


class DosenBase(BaseModel):
    nidn: str = Field(..., max_length=20)
    nama: str = Field(..., max_length=200)
    email: Optional[str] = None
    jabatan: Optional[str] = None


class DosenCreate(DosenBase):
    pass


class DosenUpdate(BaseModel):
    nidn: Optional[str] = None
    nama: Optional[str] = None
    email: Optional[str] = None
    jabatan: Optional[str] = None


class DosenOut(DosenBase):
    id: int
    class Config:
        from_attributes = True


class TahunAkademikBase(BaseModel):
    kode: str = Field(..., max_length=30)
    tahun_mulai: int
    semester: str = Field(..., pattern="^(Ganjil|Genap)$")
    tgl_mulai: Optional[date] = None
    tgl_selesai: Optional[date] = None
    aktif: bool = False


class TahunAkademikCreate(TahunAkademikBase):
    pass


class TahunAkademikUpdate(BaseModel):
    kode: Optional[str] = None
    tahun_mulai: Optional[int] = None
    semester: Optional[str] = None
    tgl_mulai: Optional[date] = None
    tgl_selesai: Optional[date] = None
    aktif: Optional[bool] = None


class TahunAkademikOut(TahunAkademikBase):
    id: int
    class Config:
        from_attributes = True


class KelasBase(BaseModel):
    mk_id: int
    tahun_akademik_id: int
    dosen_id: Optional[int] = None
    kode_kelas: str = Field(..., max_length=20)
    kapasitas: int = 40
    jadwal: Optional[str] = None
    ruang: Optional[str] = None


class KelasCreate(KelasBase):
    pass


class KelasUpdate(BaseModel):
    dosen_id: Optional[int] = None
    kode_kelas: Optional[str] = None
    kapasitas: Optional[int] = None
    jadwal: Optional[str] = None
    ruang: Optional[str] = None


class KelasOut(KelasBase):
    id: int
    class Config:
        from_attributes = True