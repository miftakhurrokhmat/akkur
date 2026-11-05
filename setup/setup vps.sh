mkdir simkur && cd simkur
# copy semua file dari 4 pesan

docker compose up -d --build
docker compose exec app alembic upgrade head
docker compose exec app python seed_data.py
docker compose exec app python seed_demo.py