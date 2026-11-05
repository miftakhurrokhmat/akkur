import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import engine, Base
from . import models  # noqa: pastikan models diimport agar ter-register

# (routers akan diimport di Pesan 2)
from .routers import (
    auth, cpl, cpmk, sub_cpmk, mk, pemetaan,
    mahasiswa, dosen, tahun_akademik, kelas,
    krs, konfigurasi, nilai, laporan,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SIMKUR API",
    version="1.0.0",
    description="Sistem Informasi Manajemen Kurikulum — Program Studi Teknologi Informasi",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
for r in [
    auth.router, cpl.router, cpmk.router, sub_cpmk.router, mk.router,
    pemetaan.router, mahasiswa.router, dosen.router, tahun_akademik.router,
    kelas.router, krs.router, konfigurasi.router, nilai.router, laporan.router,
]:
    app.include_router(r)


@app.get("/api/health", tags=["Health"])
def health():
    return {"status": "ok", "app": "SIMKUR", "version": "1.0.0"}


# Sajikan frontend dari folder static
if os.path.isdir("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")