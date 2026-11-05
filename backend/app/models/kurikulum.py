from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, Table, DateTime,
)
from sqlalchemy.orm import relationship
from ..database import Base

# Relasi many-to-many CPMK <-> MK
cpmk_mk = Table(
    "cpmk_mk", Base.metadata,
    Column("cpmk_id", Integer, ForeignKey("cpmk.id", ondelete="CASCADE"), primary_key=True),
    Column("mk_id", Integer, ForeignKey("mk.id", ondelete="CASCADE"), primary_key=True),
)


class CPL(Base):
    __tablename__ = "cpl"
    id = Column(Integer, primary_key=True)
    kode = Column(String(20), unique=True, nullable=False, index=True)
    deskripsi = Column(Text, nullable=False)
    aspek = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)

    cpmk_list = relationship("CPMK", back_populates="cpl", cascade="all, delete-orphan")


class CPMK(Base):
    __tablename__ = "cpmk"
    id = Column(Integer, primary_key=True)
    kode = Column(String(20), unique=True, nullable=False, index=True)
    deskripsi = Column(Text, nullable=False)
    cpl_id = Column(Integer, ForeignKey("cpl.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    cpl = relationship("CPL", back_populates="cpmk_list")
    sub_cpmk_list = relationship("SubCPMK", back_populates="cpmk", cascade="all, delete-orphan")
    mk_list = relationship("MK", secondary=cpmk_mk, back_populates="cpmk_list")


class SubCPMK(Base):
    __tablename__ = "sub_cpmk"
    id = Column(Integer, primary_key=True)
    kode = Column(String(50), nullable=False)
    deskripsi = Column(Text, nullable=False)
    cpmk_id = Column(Integer, ForeignKey("cpmk.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    cpmk = relationship("CPMK", back_populates="sub_cpmk_list")


class MK(Base):
    __tablename__ = "mk"
    id = Column(Integer, primary_key=True)
    kode = Column(String(20), unique=True, nullable=False, index=True)
    nama = Column(String(200), nullable=False)
    sks = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    cpmk_list = relationship("CPMK", secondary=cpmk_mk, back_populates="mk_list")
    kelas_list = relationship("Kelas", back_populates="mk")