# 1. Buat folder project
mkdir simkur && cd simkur
mkdir -p backend/app/{models,schemas,crud,services,routers,core,utils}
mkdir -p backend/{alembic/versions,static}
mkdir -p postman

# 2. Copy semua file dari 4 pesan ke folder yang sesuai

# 3. Setup database
sudo -u postgres psql -c "CREATE USER kurikulum WITH PASSWORD 'kurikulum123';"
sudo -u postgres psql -c "CREATE DATABASE sim_kurikulum OWNER kurikulum;"

# 4. Setup Python
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# 5. Migration
alembic upgrade head

# 6. Seed
python seed_data.py
python seed_demo.py

# 7. Run
uvicorn app.main:app --reload