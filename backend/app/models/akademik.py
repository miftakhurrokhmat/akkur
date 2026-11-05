from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Boolean, Date, DateTime,
)
from sqlalchemy.orm import relationship
from ..database import Base


class Mahasiswa(Base):
    __tablename__ = "mahasiswa"
    id = Column(Integer, primary_key=True)
    nim = Column(String(20), unique=True, nullable=False, index=True)
    nama = Column(String(200), nullable=False)
    angkatan = Column(Integer, nullable=False, index=True)
    prodi = Column(String(100))
    status = Column(String(20), default="aktif")
    created_at = Column(DateTime, default=datetime.now)

    krs_list = relationship("KRS", back_populates="mahasiswa", cascade="all, delete-orphan")
    ketercapaian_list = relationship("KetercapaianCPL", back_populates="mahasiswa",
                                     cascade="all, delete-orphan")


class Dosen(Base):
    __tablename__ = "dosen"
    id = Column(Integer, primary_key=True)
    nidn = Column(String(20), unique=True, nullable=False, index=True)
    nama = Column(String(200), nullable=False)
    email = Column(String(100))
    jabatan = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)

    kelas_list = relationship("Kelas", back_populates="dosen")


class TahunAkademik(Base):
    __tablename__ = "tahun_akademik"
    id = Column(Integer, primary_key=True)
    kode = Column(String(30), unique=True, nullable=False)
    tahun_mulai = Column(Integer, nullable=False)
    semester = Column(String(10), nullable=False)
    tgl_mulai = Column(Date)
    tgl_selesai = Column(Date)
    aktif = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)

    kelas_list = relationship("Kelas", back_populates="tahun_akademik")
    krs_list = relationship("KRS", back_populates="tahun_akademik")


class Kelas(Base):
    __tablename__ = "kelas"
    id = Column(Integer, primary_key=True)
    mk_id = Column(Integer, ForeignKey("mk.id"), nullable=False)
    tahun_akademik_id = Column(Integer, ForeignKey("tahun_akademik.id"), nullable=False)
    dosen_id = Column(Integer, ForeignKey("dosen.id"))
    kode_kelas = Column(String(20), nullable=False)
    kapasitas = Column(Integer, default=40)
    jadwal = Column(String(100))
    ruang = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)

    mk = relationship("MK", back_populates="kelas_list")
    tahun_akademik = relationship("TahunAkademik", back_populates="kelas_list")
    dosen = relationship("Dosen", back_populates="kelas_list")
    krs_detail_list = relationship("KRSDetail", back_populates="kelas")
    bobot_komponen_list = relationship("BobotKomponenMK", back_populates="kelas",
                                       cascade="all, delete-orphan")
    bobot_cpmk_list = relationship("BobotCPMKMK", back_populates="kelas",
                                   cascade="all, delete-orphan")
    konfigurasi_list = relationship("KonfigurasiPenilaianCPMK", back_populates="kelas",
                                    cascade="all, delete-orphan")