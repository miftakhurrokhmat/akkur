from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Date, DateTime, UniqueConstraint,
)
from sqlalchemy.orm import relationship
from ..database import Base


class KRS(Base):
    __tablename__ = "krs"
    id = Column(Integer, primary_key=True)
    mahasiswa_id = Column(Integer, ForeignKey("mahasiswa.id", ondelete="CASCADE"),
                          nullable=False)
    tahun_akademik_id = Column(Integer, ForeignKey("tahun_akademik.id"), nullable=False)
    tanggal_isi = Column(Date)
    status = Column(String(20), default="draft")
    total_sks = Column(Integer, default=0)
    approved_by = Column(Integer, ForeignKey("dosen.id"))
    approved_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (UniqueConstraint("mahasiswa_id", "tahun_akademik_id"),)

    mahasiswa = relationship("Mahasiswa", back_populates="krs_list")
    tahun_akademik = relationship("TahunAkademik", back_populates="krs_list")
    detail_list = relationship("KRSDetail", back_populates="krs",
                               cascade="all, delete-orphan")


class KRSDetail(Base):
    __tablename__ = "krs_detail"
    id = Column(Integer, primary_key=True)
    krs_id = Column(Integer, ForeignKey("krs.id", ondelete="CASCADE"), nullable=False)
    kelas_id = Column(Integer, ForeignKey("kelas.id"), nullable=False)
    status = Column(String(20), default="aktif")
    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (UniqueConstraint("krs_id", "kelas_id"),)

    krs = relationship("KRS", back_populates="detail_list")
    kelas = relationship("Kelas", back_populates="krs_detail_list")
    nilai_komponen_list = relationship("NilaiKomponen", back_populates="krs_detail",
                                       cascade="all, delete-orphan")
    nilai_cpmk_list = relationship("NilaiCPMK", back_populates="krs_detail",
                                   cascade="all, delete-orphan")
    nilai_mk = relationship("NilaiMK", back_populates="krs_detail",
                            uselist=False, cascade="all, delete-orphan")