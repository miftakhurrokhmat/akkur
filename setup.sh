#!/bin/bash
# =====================================================================
# SIMKUR — Setup Script (Linux/Mac)
# =====================================================================
set -e

echo "🚀 SIMKUR Setup — Localhost"
echo "================================"

# 1. Cek prasyarat
echo "📋 Cek prasyarat..."
command -v python3 >/dev/null || { echo "❌ Python 3 tidak ditemukan"; exit 1; }
command -v psql >/dev/null || { echo "❌ PostgreSQL tidak ditemukan"; exit 1; }

# 2. Setup database
echo "🗄️  Setup database..."
sudo -u postgres psql <<EOF || echo "⚠️  User/database mungkin sudah ada, skip"
CREATE USER kurikulum WITH PASSWORD 'kurikulum123';
CREATE DATABASE sim_kurikulum OWNER kurikulum;
GRANT ALL PRIVILEGES ON DATABASE sim_kurikulum TO kurikulum;
EOF

# 3. Setup Python venv
echo "🐍 Setup Python environment..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q

# 4. Copy .env
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ .env dibuat dari .env.example"
fi

# 5. Migration
echo "🔄 Menjalankan migration..."
alembic upgrade head

# 6. Seed
echo "🌱 Seed data kurikulum (mungkin 10-20 detik)..."
python seed_data.py

echo "🌱 Seed data demo (opsional)..."
python seed_demo.py

# 7. Ringkasan
echo ""
echo "================================"
echo "✅ SETUP SELESAI"
echo "================================"
echo "Jalankan server dengan:"
echo "  source backend/venv/bin/activate"
echo "  cd backend && uvicorn app.main:app --reload"
echo ""
echo "Buka: http://localhost:8000"
echo ""
echo "Login:"
echo "  admin / admin123  (Admin Prodi)"
echo "  dewi  / dosen123  (Dosen)"
echo "  budi  / mhs123    (Mahasiswa)"
echo "================================"