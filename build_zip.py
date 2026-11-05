"""
Script untuk membuat file ZIP berisi semua kode Python SIMKUR.
Jalankan: python build_zip.py
"""
import os
import zipfile
from pathlib import Path

# File-file Python yang akan dimasukkan ke ZIP
# (Semua file dari Pesan 1-4)
FILES = {
    # ===== Config =====
    "backend/requirements.txt": """fastapi==0.115.0
uvicorn[standard]==0.32.0
sqlalchemy==2.0.36
alembic==1.13.3
psycopg2-binary==2.9.10
pydantic==2.9.2
pydantic-settings==2.6.0
python-dotenv==1.0.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.12
openpyxl==3.1.5
""",
    "backend/.env.example": """DATABASE_URL=postgresql://kurikulum:kurikulum123@localhost:5432/sim_kurikulum
SECRET_KEY=ganti-ini-dengan-random-string-panjang
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
""",
    "backend/alembic.ini": """[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
""",

    # ===== App core =====
    "backend/app/__init__.py": "# SIMKUR Backend\n__version__ = '1.0.0'\n",
    "backend/app/database.py": open("backend/app/database.py").read() if os.path.exists("backend/app/database.py") else "# isi database.py",
    "backend/app/main.py": open("backend/app/main.py").read() if os.path.exists("backend/app/main.py") else "# isi main.py",

    # ===== README =====
    "README.md": "# SIMKUR\n\nSistem Informasi Manajemen Kurikulum.\n\nLihat file di `backend/` untuk kode utama.\n",
}

# File-file dari Pesan 1-4 (dalam bentuk string literal)
# Karena sangat panjang, simpan di file terpisah `_files_content.py`
try:
    from _files_content import ALL_FILES
    FILES.update(ALL_FILES)
    print(f"✅ Loaded {len(ALL_FILES)} files dari _files_content.py")
except ImportError:
    print("⚠️  _files_content.py tidak ditemukan, hanya config yang di-zip")


def build():
    out = Path("simkur.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path, content in FILES.items():
            zf.writestr(path, content)
    size_kb = out.stat().st_size / 1024
    print(f"\n✅ ZIP dibuat: {out.absolute()}")
    print(f"   Ukuran: {size_kb:.1f} KB")
    print(f"   File  : {len(FILES)}")


if __name__ == "__main__":
    build()