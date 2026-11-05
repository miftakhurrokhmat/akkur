.PHONY: help install migrate seed run docker-up docker-down test clean

help:
	@echo "SIMKUR — Makefile"
	@echo "================="
	@echo "make install     — Install dependencies"
	@echo "make migrate     — Jalankan migration"
	@echo "make seed        — Seed data"
	@echo "make run         — Jalankan dev server"
	@echo "make docker-up   — Deploy via Docker"
	@echo "make docker-down — Stop Docker"
	@echo "make clean       — Bersihkan cache"

install:
	cd backend && python -m venv venv && \
		. venv/bin/activate && \
		pip install -r requirements.txt

migrate:
	cd backend && . venv/bin/activate && alembic upgrade head

seed:
	cd backend && . venv/bin/activate && python seed_data.py
	cd backend && . venv/bin/activate && python seed_demo.py

run:
	cd backend && . venv/bin/activate && uvicorn app.main:app --reload

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf backend/venv