from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, Numeric, Boolean,
    DateTime, UniqueConstraint,
)
from sqlalchemy.orm import relationship
from ..database import Base


class KomponenPenilaian(Base):
    __tablename__ = "komponen_penilaian"
    id = Column(Integer, primary_key=True)
    kode = Column(String(30), unique=True, nullable=False)
    nama = Column(String(100), nullable=False)
    kategori = Column(String(30))
    deskripsi = Column(Text)
    aktif = Column(Boolean, default=True)


class BobotKomponenMK(Base):
    __tablename__ = "bobot_komponen_mk"
    id = Column(Integer, primary_key=True)
    kelas_id = Column(Integer, ForeignKey("kelas.id", ondelete="CASCADE"), nullable=False)
    komponen_id = Column(Integer, ForeignKey("komponen_penilaian.id"), nullable=False)
    bobot = Column(Numeric(5, 2), nullable=False)

    __table_args__ = (UniqueConstraint("kelas_id", "komponen_id"),)

    kelas = relationship("Kelas", back_populates="bobot_komponen_list")
    komponen = relationship("KomponenPenilaian")


class BobotCPMKMK(Base):
    __tablename__ = "bobot_cpmk_mk"
    id = Column(Integer, primary_key=True)
    kelas_id = Column(Integer, ForeignKey("kelas.id", ondelete="CASCADE"), nullable=False)
    cpmk_id = Column(Integer, ForeignKey("cpmk.id"), nullable=False)
    bobot = Column(Numeric(5, 2), nullable=False)

    __table_args__ = (UniqueConstraint("kelas_id", "cpmk_id"),)

    kelas = relationship("Kelas", back_populates="bobot_cpmk_list")
    cpmk = relationship("CPMK")


class KonfigurasiPenilaianCPMK(Base):
    __tablename__ = "konfigurasi_penilaian_cpmk"
    id = Column(Integer, primary_key=True)
    kelas_id = Column(Integer, ForeignKey("kelas.id", ondelete="CASCADE"), nullable=False)
    cpmk_id = Column(Integer, ForeignKey("cpmk.id"), nullable=False)
    komponen_id = Column(Integer, ForeignKey("komponen_penilaian.id"), nullable=False)
    tahap = Column(String(50))
    teknik = Column(String(100))
    instrumen = Column(Text)
    kriteria = Column(Text)
    bobot = Column(Numeric(5, 2), nullable=False)

    __table_args__ = (UniqueConstraint("kelas_id", "cpmk_id", "komponen_id"),)

    kelas = relationship("Kelas", back_populates="konfigurasi_list")
    cpmk = relationship("CPMK")
    komponen = relationship("KomponenPenilaian")


class NilaiKomponen(Base):
    __tablename__ = "nilai_komponen"
    id = Column(Integer, primary_key=True)
    krs_detail_id = Column(Integer, ForeignKey("krs_detail.id", ondelete="CASCADE"),
                           nullable=False)
    komponen_id = Column(Integer, ForeignKey("komponen_penilaian.id"), nullable=False)
    nilai = Column(Numeric(5, 2))
    catatan = Column(Text)
    updated_by = Column(Integer, ForeignKey("dosen.id"))
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (UniqueConstraint("krs_detail_id", "komponen_id"),)

    krs_detail = relationship("KRSDetail", back_populates="nilai_komponen_list")
    komponen = relationship("KomponenPenilaian")


class NilaiCPMK(Base):
    __tablename__ = "nilai_cpmk"
    id = Column(Integer, primary_key=True)
    krs_detail_id = Column(Integer, ForeignKey("krs_detail.id", ondelete="CASCADE"),
                           nullable=False)
    cpmk_id = Column(Integer, ForeignKey("cpmk.id"), nullable=False)
    nilai = Column(Numeric(5, 2))

    __table_args__ = (UniqueConstraint("krs_detail_id", "cpmk_id"),)

    krs_detail = relationship("KRSDetail", back_populates="nilai_cpmk_list")
    cpmk = relationship("CPMK")


class NilaiMK(Base):
    __tablename__ = "nilai_mk"
    id = Column(Integer, primary_key=True)
    krs_detail_id = Column(Integer, ForeignKey("krs_detail.id", ondelete="CASCADE"),
                           nullable=False, unique=True)
    nilai_angka = Column(Numeric(5, 2))
    nilai_huruf = Column(String(3))
    bobot_nilai = Column(Numeric(4, 2))
    lulus = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    krs_detail = relationship("KRSDetail", back_populates="nilai_mk")


class KetercapaianCPL(Base):
    __tablename__ = "ketercapaian_cpl"
    id = Column(Integer, primary_key=True)
    mahasiswa_id = Column(Integer, ForeignKey("mahasiswa.id", ondelete="CASCADE"),
                          nullable=False)
    cpl_id = Column(Integer, ForeignKey("cpl.id"), nullable=False)
    tahun_akademik_id = Column(Integer, ForeignKey("tahun_akademik.id"), nullable=False)
    skor_maks = Column(Numeric(8, 2), default=0)
    total_skor = Column(Numeric(8, 2), default=0)
    nilai_rata_rata = Column(Numeric(5, 2))
    status = Column(String(20))

    __table_args__ = (UniqueConstraint("mahasiswa_id", "cpl_id", "tahun_akademik_id"),)

    mahasiswa = relationship("Mahasiswa", back_populates="ketercapaian_list")
    cpl = relationship("CPL")