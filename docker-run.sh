#!/bin/bash
# =====================================================================
# SIMKUR — Docker Deployment Script
# =====================================================================
set -e

echo "🐳 SIMKUR Docker Deployment"
echo "================================"

# 1. Cek Docker
command -v docker >/dev/null || { echo "❌ Docker tidak ditemukan"; exit 1; }
command -v docker-compose >/dev/null || docker compose version >/dev/null || {
    echo "❌ docker-compose tidak ditemukan"; exit 1;
}

# 2. Copy .env
if [ ! -f .env ]; then
    cp backend/.env.example .env
    echo "✅ .env dibuat. Edit jika perlu."
fi

# 3. Build & up
echo "🔨 Building images..."
docker compose build

echo "🚀 Starting services..."
docker compose up -d

echo "⏳ Menunggu database siap..."
sleep 10

# 4. Migration & seed
echo "🔄 Migration..."
docker compose exec -T app alembic upgrade head

echo "🌱 Seed data..."
docker compose exec -T app python seed_data.py
docker compose exec -T app python seed_demo.py

# 5. Status
echo ""
echo "================================"
echo "✅ DEPLOYMENT SELESAI"
echo "================================"
docker compose ps
echo ""
echo "Akses:"
echo "  Frontend : http://localhost"
echo "  API Docs : http://localhost/docs"
echo "  Health   : http://localhost/api/health"
echo ""
echo "Login:"
echo "  admin / admin123"
echo "  dewi  / dosen123"
echo "  budi  / mhs123"
echo "================================"