# SIMKUR — Sistem Informasi Manajemen Kurikulum

Aplikasi manajemen kurikulum berbasis web untuk Program Studi Teknologi Informasi.

## Fitur

- ✅ Master Kurikulum: CPL, CPMK, Sub-CPMK, MK, Pemetaan CPMK↔MK
- ✅ Master Akademik: Mahasiswa, Dosen, Tahun Akademik, Kelas
- ✅ Transaksi KRS: buat, ajukan, setujui
- ✅ Penilaian: konfigurasi bobot, input nilai, kalkulasi otomatis
- ✅ Laporan: Tabel 19 (MK), Tabel 20 (CPL), transkrip, distribusi
- ✅ Export Excel
- ✅ Auth JWT
- ✅ Docker-ready

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy 2.0, Alembic
- **Database**: PostgreSQL 16
- **Frontend**: HTML + Tailwind (CDN)
- **Deploy**: Docker Compose + Nginx

## Struktur

Lihat dokumentasi lengkap di PRD & SAD.

## Quick Start (Localhost)

### 1. Prasyarat
- Python 3.10+
- PostgreSQL 14+

### 2. Setup database
```bash
sudo -u postgres psql
CREATE USER kurikulum WITH PASSWORD 'kurikulum123';
CREATE DATABASE sim_kurikulum OWNER kurikulum;
\q