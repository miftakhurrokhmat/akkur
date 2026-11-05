from pydantic import BaseModel, Field
from typing import Optional, List


# ============ CPL ============
class CPLBase(BaseModel):
    kode: str = Field(..., max_length=20)
    deskripsi: str
    aspek: Optional[str] = None


class CPLCreate(CPLBase):
    pass


class CPLUpdate(BaseModel):
    kode: Optional[str] = None
    deskripsi: Optional[str] = None
    aspek: Optional[str] = None


class CPLOut(CPLBase):
    id: int
    class Config:
        from_attributes = True


# ============ CPMK ============
class CPMKBase(BaseModel):
    kode: str = Field(..., max_length=20)
    deskripsi: str
    cpl_id: int


class CPMKCreate(CPMKBase):
    pass


class CPMKUpdate(BaseModel):
    kode: Optional[str] = None
    deskripsi: Optional[str] = None
    cpl_id: Optional[int] = None


class CPMKOut(CPMKBase):
    id: int
    class Config:
        from_attributes = True


# ============ SubCPMK ============
class SubCPMKBase(BaseModel):
    kode: str = Field(..., max_length=50)
    deskripsi: str
    cpmk_id: int


class SubCPMKCreate(SubCPMKBase):
    pass


class SubCPMKUpdate(BaseModel):
    kode: Optional[str] = None
    deskripsi: Optional[str] = None
    cpmk_id: Optional[int] = None


class SubCPMKOut(SubCPMKBase):
    id: int
    class Config:
        from_attributes = True


# ============ MK ============
class MKBase(BaseModel):
    kode: str = Field(..., max_length=20)
    nama: str = Field(..., max_length=200)
    sks: int = Field(..., gt=0, le=10)
    semester: int = Field(..., ge=1, le=8)


class MKCreate(MKBase):
    pass


class MKUpdate(BaseModel):
    kode: Optional[str] = None
    nama: Optional[str] = None
    sks: Optional[int] = None
    semester: Optional[int] = None


class MKOut(MKBase):
    id: int
    class Config:
        from_attributes = True


# ============ Pemetaan ============
class PemetaanCreate(BaseModel):
    cpmk_id: int
    mk_id: int