@echo off
REM =====================================================================
REM SIMKUR — Setup Script (Windows)
REM =====================================================================
echo.
echo SIMKUR Setup - Localhost
echo ================================
echo.

REM 1. Cek prasyarat
echo [1/6] Cek prasyarat...
where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python tidak ditemukan
    exit /b 1
)
where psql >nul 2>nul
if errorlevel 1 (
    echo WARNING: psql tidak ditemukan, pastikan PostgreSQL terinstal
)

REM 2. Setup database (manual karena butuh password)
echo.
echo [2/6] Setup database...
echo Jalankan manual via pgAdmin atau psql:
echo   CREATE USER kurikulum WITH PASSWORD 'kurikulum123';
echo   CREATE DATABASE sim_kurikulum OWNER kurikulum;
pause

REM 3. Setup Python venv
echo.
echo [3/6] Setup Python environment...
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install --upgrade pip -q
pip install -r requirements.txt -q

REM 4. Copy .env
if not exist .env (
    copy .env.example .env
    echo .env dibuat dari .env.example
)

REM 5. Migration
echo.
echo [5/6] Menjalankan migration...
alembic upgrade head

REM 6. Seed
echo.
echo [6/6] Seed data...
python seed_data.py
python seed_demo.py

echo.
echo ================================
echo SETUP SELESAI
echo ================================
echo Jalankan server dengan:
echo   cd backend
echo   venv\Scripts\activate.bat
echo   uvicorn app.main:app --reload
echo.
echo Buka: http://localhost:8000
echo.
echo Login:
echo   admin / admin123  (Admin Prodi)
echo   dewi  / dosen123  (Dosen)
echo   budi  / mhs123    (Mahasiswa)
echo ================================
pause